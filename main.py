import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from urllib.parse import urljoin
import json


class KPKLelangScraper:
    def __init__(self):
        self.base_url = "https://www.kpk.go.id"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "id,en-US;q=0.7,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            }
        )

    def get_announcement_pages(self):
        """Mendapatkan semua halaman pengumuman lelang"""
        announcements = []

        # URL utama pengumuman lelang
        url = f"{self.base_url}/id/ruang-informasi/pengumuman/lelang-barang-rampasan"

        try:
            print("📄 Mengambil halaman utama lelang...")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Simpan HTML untuk debugging
            with open("debug_lelang_page.html", "w", encoding="utf-8") as f:
                f.write(soup.prettify())
            print("💾 HTML disimpan ke debug_lelang_page.html")

            # Extract data dari halaman utama
            page_announcements = self.extract_lelang_data(soup)
            announcements.extend(page_announcements)

            print(f"✅ Ditemukan {len(page_announcements)} lelang di halaman utama")

        except requests.RequestException as e:
            print(f"❌ Error mengambil halaman: {e}")

        return announcements

    def extract_lelang_data(self, soup):
        """Extract data lelang dari halaman"""
        announcements = []

        # Cari semua card pengumuman lelang berdasarkan struktur HTML yang diberikan
        lelang_cards = soup.find_all("div", class_="card-pengumuman")

        if not lelang_cards:
            # Coba selector alternatif
            lelang_cards = soup.find_all(
                "div", class_=lambda x: x and "card" in x.lower()
            )
            print(
                f"🔍 Mencari dengan selector alternatif, ditemukan: {len(lelang_cards)} cards"
            )

        print(f"🎯 Ditemukan {len(lelang_cards)} card lelang")

        for i, card in enumerate(lelang_cards):
            try:
                print(f"  Processing lelang {i + 1}/{len(lelang_cards)}...")

                # Extract data dari card
                lelang_data = self.extract_card_data(card)
                if lelang_data and lelang_data.get("judul"):
                    announcements.append(lelang_data)
                    print(f"    ✅ {lelang_data['judul'][:50]}...")
                else:
                    print(f"    ⚠️  Data tidak lengkap, skip")

            except Exception as e:
                print(f"    ❌ Error processing card {i + 1}: {e}")
                continue

        return announcements

    def extract_card_data(self, card):
        """Extract data detail dari card lelang"""
        data = {
            "judul": "",
            "link": "",
            "status": "",
            "jumlah_object": "",
            "tanggal_lelang": "",
            "waktu_lelang": "",
            "lokasi": "",
            "situs_lelang": "",
            "preview": "",
        }

        try:
            # Extract judul
            title_elem = card.select_one("a.d-block.h5")
            if not title_elem:
                title_elem = card.find("a", class_=lambda x: x and "text-black" in x)
            if not title_elem:
                title_elem = card.find("h5") or card.find("h4") or card.find("h3")
            if not title_elem:
                # Cari link pertama dengan teks panjang
                links = card.find_all("a", href=True)
                for link in links:
                    if len(link.get_text(strip=True)) > 20:
                        title_elem = link
                        break

            if title_elem:
                data["judul"] = title_elem.get_text(strip=True)
                # Extract link
                href = title_elem.get("href", "")
                if href:
                    if href.startswith("/"):
                        data["link"] = urljoin(self.base_url, href)
                    else:
                        data["link"] = href

            # Extract status lelang
            status_elem = card.select_one("span.btn.btn-alert-red")
            if status_elem:
                data["status"] = status_elem.get_text(strip=True)
            else:
                # Cari teks status lainnya
                status_texts = card.find_all(
                    text=re.compile(r"lelang.*ditutup|lelang.*dibuka", re.I)
                )
                if status_texts:
                    data["status"] = status_texts[0].strip()

            # Extract jumlah object
            object_elem = card.select_one("span.btn.btn--ghost-muted-grey")
            if object_elem:
                object_text = object_elem.get_text(strip=True)
                # Extract angka dari teks
                match = re.search(r"(\d+)\s*Objek", object_text)
                if match:
                    data["jumlah_object"] = match.group(1)

            # Extract tanggal dan waktu lelang
            date_elems = card.find_all(
                text=re.compile(
                    r"\d{1,2}\s+[A-Za-z]+\s+-\s+\d{1,2}\s+[A-Za-z]+\s+\d{4}"
                )
            )
            time_elems = card.find_all(
                text=re.compile(r"\d{1,2}:\d{2}\s+-\s+\d{1,2}:\d{2}")
            )

            if date_elems:
                data["tanggal_lelang"] = date_elems[0].strip()
            if time_elems:
                data["waktu_lelang"] = time_elems[0].strip()

            # Extract lokasi dan situs lelang
            location_elem = card.find("i", class_="bzi-map-marker")
            if location_elem:
                location_parent = location_elem.find_parent("div")
                if location_parent:
                    location_text = location_parent.get_text(strip=True)
                    # Pisahkan lokasi fisik dan situs lelang
                    if "lelang.go.id" in location_text:
                        parts = location_text.split("lelang.go.id")
                        data["lokasi"] = parts[0].strip()
                        data["situs_lelang"] = "lelang.go.id" + (
                            parts[1] if len(parts) > 1 else ""
                        )
                    else:
                        data["lokasi"] = location_text

            # Extract preview/deskripsi singkat
            preview_elem = card.select_one("span.d-block.mb-0.text-limiter-3")
            if preview_elem:
                data["preview"] = preview_elem.get_text(strip=True)
            else:
                # Ambil semua teks dari card sebagai fallback
                all_text = card.get_text(strip=True)
                # Hapus judul dan informasi yang sudah di-extract
                texts_to_remove = [
                    data["judul"],
                    data["status"],
                    data["tanggal_lelang"],
                    data["waktu_lelang"],
                ]
                for text in texts_to_remove:
                    if text:
                        all_text = all_text.replace(text, "")
                data["preview"] = " ".join(all_text.split()[:30])  # Batasi panjang

            # Analisis tambahan dari judul
            self.analyze_judul_data(data)

        except Exception as e:
            print(f"    ⚠️  Error extracting card data: {e}")

        return data

    def analyze_judul_data(self, data):
        """Analisis data tambahan dari judul lelang"""
        judul = data["judul"].lower()

        # Extract nama pemilik dari pattern "an NAMA"
        nama_match = re.search(r"an\s+([A-Z][A-Z\s]+?)(?:\-|\d|$)", data["judul"])
        if nama_match:
            data["nama_pemilik"] = nama_match.group(1).strip()

        # Tentukan jenis lelang berdasarkan judul
        if "eksekusi" in judul:
            data["jenis_lelang"] = "Lelang Eksekusi"
        elif "rampasan" in judul:
            data["jenis_lelang"] = "Barang Rampasan"
        else:
            data["jenis_lelang"] = "Lelang Barang"

        # Extract nomor/tahun lelang
        tahun_match = re.search(r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})", data["judul"])
        if tahun_match:
            data["nomor_lelang"] = tahun_match.group(1)

    def get_detailed_lelang_info(self, url):
        """Mendapatkan informasi detail dari halaman lelang individual"""
        try:
            print(f"  🔍 Mengambil detail dari: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            detail_data = {}

            # Extract konten utama
            content_elem = soup.find(
                "div",
                class_=lambda x: x
                and ("content" in x.lower() or "article" in x.lower()),
            )
            if content_elem:
                detail_data["konten_lengkap"] = content_elem.get_text(strip=True)

            # Extract informasi tambahan seperti PDF, dokumen, dll
            pdf_links = soup.find_all("a", href=re.compile(r"\.pdf$", re.I))
            if pdf_links:
                detail_data["dokumen_pendukung"] = [
                    urljoin(url, link["href"]) for link in pdf_links
                ]

            return detail_data

        except Exception as e:
            print(f"    ❌ Error mengambil detail: {e}")
            return {}

    def save_to_excel(self, data, filename="lelang_kpk_detailed.xlsx"):
        """Simpan data ke file Excel"""
        if not data:
            print("❌ Tidak ada data untuk disimpan")
            return None

        df = pd.DataFrame(data)

        # Reorder columns untuk tampilan lebih baik
        columns_order = [
            "judul",
            "jenis_lelang",
            "status",
            "nama_pemilik",
            "jumlah_object",
            "tanggal_lelang",
            "waktu_lelang",
            "lokasi",
            "situs_lelang",
            "link",
            "preview",
        ]

        # Hanya ambil columns yang ada
        existing_columns = [col for col in columns_order if col in df.columns]
        df = df[existing_columns]

        # Save to Excel
        try:
            with pd.ExcelWriter(filename, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Data Lelang KPK", index=False)

                # Auto-adjust column widths
                worksheet = writer.sheets["Data Lelang KPK"]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width

            print(f"💾 Data disimpan ke: {filename}")
            return filename

        except Exception as e:
            print(f"❌ Error menyimpan Excel: {e}")
            # Fallback to CSV
            try:
                csv_file = filename.replace(".xlsx", ".csv")
                df.to_csv(csv_file, index=False, encoding="utf-8-sig")
                print(f"💾 Data disimpan ke CSV: {csv_file}")
                return csv_file
            except Exception as e2:
                print(f"❌ Error menyimpan CSV: {e2}")
                return None

    def display_summary(self, data):
        """Tampilkan summary data"""
        if not data:
            print("❌ Tidak ada data lelang ditemukan")
            return

        print(f"\n{'=' * 60}")
        print("📊 SUMMARY DATA LELANG BARANG RAMPASAN KPK")
        print(f"{'=' * 60}")
        print(f"Total lelang ditemukan: {len(data)}")

        # Statistik status
        status_counts = {}
        for item in data:
            status = item.get("status", "Tidak Diketahui")
            status_counts[status] = status_counts.get(status, 0) + 1

        print(f"\n📊 Status Lelang:")
        for status, count in status_counts.items():
            print(f"   - {status}: {count}")

        # Statistik jumlah object
        total_objects = sum(
            int(item["jumlah_object"]) for item in data if item["jumlah_object"]
        )
        print(f"\n📦 Total Object Lelang: {total_objects}")

        print(f"\n📋 Contoh data lelang:")
        for i, item in enumerate(data[:3], 1):
            print(f"\n{i}. {item['judul'][:80]}...")
            print(f"   Status: {item.get('status', 'N/A')}")
            print(f"   Object: {item.get('jumlah_object', 'N/A')}")
            print(f"   Tanggal: {item.get('tanggal_lelang', 'N/A')}")
            if item.get("nama_pemilik"):
                print(f"   Pemilik: {item['nama_pemilik']}")

    def run(self):
        """Jalankan scraping process"""
        print("🔍 MEMULAI SCRAPING LELANG BARANG RAMPASAN KPK")
        print(
            "🌐 Sumber: https://www.kpk.go.id/id/ruang-informasi/pengumuman/lelang-barang-rampasan"
        )
        print(f"{'=' * 60}")

        # Dapatkan data lelang
        lelang_data = self.get_announcement_pages()

        if not lelang_data:
            print("❌ Tidak ada data lelang yang ditemukan")
            print(
                "💡 Tips: Check file debug_lelang_page.html untuk analisis struktur HTML"
            )
            return

        print(f"\n✅ Berhasil mengumpulkan {len(lelang_data)} data lelang")

        # Tampilkan summary
        self.display_summary(lelang_data)

        # Simpan ke Excel
        filename = self.save_to_excel(lelang_data)

        if filename:
            print(f"\n🎉 Proses selesai! File tersimpan sebagai: {filename}")

            # Tampilkan path file
            import os

            file_path = os.path.abspath(filename)
            print(f"📁 Lokasi file: {file_path}")
        else:
            print(f"\n⚠️  Proses selesai tetapi ada masalah menyimpan file")


def main():
    """Main function"""
    try:
        scraper = KPKLelangScraper()
        scraper.run()
    except KeyboardInterrupt:
        print("\n\n⏹️  Program dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
