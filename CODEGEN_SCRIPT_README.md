# Codegen Script Folder

## Apa itu folder `codegen_script`?

Folder ini menyimpan **script asli hasil recording Playwright** sebelum di-enhance/generate. Script-script ini adalah versi murni dari Playwright codegen yang bisa digunakan kembali untuk membuat test dengan konfigurasi berbeda.

## Struktur Folder

```
codegen_script/
├── login_20250112_143022.py          # Script recording login
├── search_products_20250112_150135.py # Script recording search
└── checkout_20250112_153045.py        # Script recording checkout
```

Setiap file memiliki format: `{test_name}_{timestamp}.py`

## Cara Kerja

### 1. Mode Recording (Record New Test)
Ketika Anda merekam test baru:
1. Script asli disimpan di folder `codegen_script/` dengan timestamp
2. Script yang sama di-copy ke folder test (misalnya `e2e/p1-regression/login/tests/`)
3. Script di folder test kemudian di-enhance (ditambahkan waits, markers, dll)

**Hasil:**
- ✅ Script asli tetap tersimpan di `codegen_script/`
- ✅ Script enhanced ada di folder test

### 2. Mode Generate (Generate from Existing Script)
Jika Anda sudah punya script di `codegen_script/`, Anda bisa:
1. Pilih mode "Generate from existing script"
2. Pilih script yang sudah ada
3. Script akan di-copy ke folder test baru dengan priority yang berbeda
4. Script kemudian di-enhance sesuai kebutuhan

**Keuntungan:**
- 🚀 Tidak perlu record ulang
- 🔄 Bisa menggunakan 1 script untuk multiple test dengan priority berbeda
- ⚡ Lebih cepat karena skip proses recording

## Contoh Penggunaan

### Scenario 1: Record Test Baru
```bash
python3 simple_recorder.py
```

**Flow:**
1. Pilih Priority: P1 - Regression
2. Pilih Mode: **1. Record new test**
3. Masukkan test name: `login`
4. Masukkan URL: `https://example.com/login`
5. Browser terbuka → Record actions → Close browser
6. Script tersimpan di:
   - `codegen_script/login_20250112_143022.py` (asli)
   - `e2e/p1-regression/login/tests/login_test.py` (enhanced)

### Scenario 2: Generate dari Script yang Sudah Ada
```bash
python3 simple_recorder.py
```

**Flow:**
1. Pilih Priority: P0 - Smoke Test
2. Pilih Mode: **2. Generate from existing script**
3. Pilih script: `login_20250112_143022.py`
4. Masukkan test name: `login_smoke`
5. Script di-copy dan enhanced ke:
   - `e2e/p0-smoke_test/login_smoke/tests/login_smoke_test.py`

### Scenario 3: Reuse Script untuk Test Regression
Anda sudah punya script login untuk smoke test, sekarang ingin membuat regression test:

```bash
python3 simple_recorder.py
```

**Flow:**
1. Pilih Priority: P1 - Regression
2. Pilih Mode: **2. Generate from existing script**
3. Pilih script: `login_20250112_143022.py`
4. Masukkan test name: `login_regression`
5. Script di-copy dan enhanced dengan marker `@pytest.mark.regression`

## Best Practices

### 1. Naming Convention
Gunakan nama yang deskriptif untuk test:
- ✅ `login_valid_credentials`
- ✅ `search_products_by_category`
- ✅ `checkout_with_discount_code`
- ❌ `test1`, `test2`

### 2. Organize by Feature
Simpan script berdasarkan fitur:
```
codegen_script/
├── login_basic_20250112.py
├── login_with_2fa_20250112.py
├── search_simple_20250112.py
└── search_advanced_filters_20250112.py
```

### 3. When to Record New vs Generate
**Record New Test:**
- Fitur baru yang belum pernah di-test
- Perlu capture interactions yang berbeda
- Update UI/UX yang signifikan

**Generate from Existing:**
- Sama script, beda priority (P0 → P1 → P2)
- Sama script, beda test organization
- Ingin test ulang dengan enhancement berbeda

### 4. Keep Scripts Updated
Jika UI berubah:
1. Record ulang script baru
2. Script lama tetap tersimpan dengan timestamp
3. Bisa compare antara versi lama dan baru

## Troubleshooting

### Folder `codegen_script` tidak ada
**Solusi:** Folder akan dibuat otomatis saat pertama kali record test.

### Tidak ada script di folder
**Solusi:** Pilih mode "Record new test" untuk membuat script pertama.

### Script tidak compatible
**Solusi:** Script mungkin untuk versi Playwright lama. Record ulang script baru.

### Strict Mode Violation - Multiple Elements Found

**Error:**
```
Error: strict mode violation: get_by_role("button", name="DELETE") resolved to 2 elements
```

**Penyebab:**
Generator mendeteksi generic button names (Delete, Cancel, OK, Save, dll) dan memberikan warning:
```python
# Wait for button to be ready and clickable - use more specific locator if needed
page.get_by_role("button", name="DELETE").wait_for(...)
```

**Solusi Manual:**
Gunakan test_id parent yang lebih spesifik (lihat error message untuk test_id):

```python
# SEBELUM (Ambiguous - 2 elements):
page.get_by_role("button", name="DELETE").wait_for(state='visible', timeout=10000)
expect(page.get_by_role("button", name="DELETE")).to_be_enabled()
page.get_by_role("button", name="DELETE").scroll_into_view_if_needed()
page.wait_for_timeout(5000)
page.get_by_role("button", name="DELETE").click(delay=200)

# SESUDAH (Specific - 1 element):
page.get_by_test_id("parent-container-div-buttons").get_by_role("button", name="DELETE").wait_for(state='visible', timeout=10000)
expect(page.get_by_test_id("parent-container-div-buttons").get_by_role("button", name="DELETE")).to_be_enabled()
page.get_by_test_id("parent-container-div-buttons").get_by_role("button", name="DELETE").scroll_into_view_if_needed()
page.wait_for_timeout(5000)
page.get_by_test_id("parent-container-div-buttons").get_by_role("button", name="DELETE").click(delay=200)
```

**Cara Cepat Find Test ID:**
Lihat error message - test_id ada di error suggestion:
```
2) <button ... data-testid="customer-organization-...-div-buttons">...
   aka get_by_test_id("customer-organization-...-div-buttons").get_by_role("button", name="DELETE")
```

## Tips

1. **Backup Scripts:** Script di `codegen_script/` sangat berharga, backup secara berkala
2. **Version Control:** Commit folder `codegen_script/` ke git
3. **Documentation:** Tambahkan komentar di script untuk menjelaskan test scenario
4. **Reusability:** Satu script bagus bisa digunakan untuk multiple test cases

## Summary

| Feature | Record New | Generate Existing |
|---------|-----------|-------------------|
| Speed | Slower (need recording) | ⚡ Faster |
| Flexibility | 🎯 Full control | ♻️ Reuse script |
| Use Case | New features | Multiple priorities |
| Browser | Opens | No need |

Happy Testing! 🎉
