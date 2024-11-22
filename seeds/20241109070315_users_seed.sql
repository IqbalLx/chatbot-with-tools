-- +goose Up
-- +goose StatementBegin
INSERT INTO users(nik, name, sex, place_of_birth, date_of_birth, profession, address, religion)
VALUES 
    ('1231234567890001', 'John Does', 'Laki-laki', 'Semarang', '2022-09-12', 'Pegawai Negeri Sipil', 'Desa Kembang Sari, Semarang', 'Islam'),
    ('1231234567890002', 'Jane Does', 'Perempuan', 'Jakarta', '2028-01-01', 'Wiraswasta', 'Desa Kumala Kumal, Jakarta', 'Katolik'),
    ('1231234567890004', 'Mikael Santori', 'Laki-laki', 'Surabaya', '2029-11-01', 'Wiraswasta', 'Disana Dimari, Kemana mana', 'Buddha')
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

-- +goose StatementEnd