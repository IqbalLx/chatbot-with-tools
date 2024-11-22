-- +goose Up
-- +goose StatementBegin
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid(),
    nik TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    sex TEXT NOT NULL,
    place_of_birth TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    profession TEXT NOT NULL,
    address TEXT NOT NULL,
    religion TEXT NOT NULL
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE IF EXISTS users;
-- +goose StatementEnd
