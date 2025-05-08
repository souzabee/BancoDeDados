CREATE TABLE IF NOT EXISTS artistas (
    artista_id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    criado_em TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nome_usuario VARCHAR(100) UNIQUE NOT NULL,
    hash_senha VARCHAR(255) NOT NULL,
    eh_administrador BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS musicas (
    musica_id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    artista_id INT,
    criado_em TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_artista
        FOREIGN KEY(artista_id)
        REFERENCES artistas(artista_id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS playlists (
    playlist_id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    proprietario_usuario_id INT NOT NULL,
    criado_em TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_proprietario_usuario
        FOREIGN KEY(proprietario_usuario_id)
        REFERENCES usuarios(usuario_id)
        ON DELETE CASCADE,
    CONSTRAINT uq_usuario_playlist_nome UNIQUE (proprietario_usuario_id, nome)
);

CREATE TABLE IF NOT EXISTS playlist_musicas (
    playlist_id INT NOT NULL,
    musica_id INT NOT NULL,
    adicionado_em TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_playlist
        FOREIGN KEY(playlist_id)
        REFERENCES playlists(playlist_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_musica
        FOREIGN KEY(musica_id) 
        REFERENCES musicas(musica_id)
        ON DELETE CASCADE,
    PRIMARY KEY (playlist_id, musica_id)
);

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_interacao_enum') THEN
        CREATE TYPE tipo_interacao_enum AS ENUM ('gostei', 'nao_gostei');
    END IF;
END$$;

CREATE TABLE IF NOT EXISTS interacoes_usuario_musica (
    usuario_id INT NOT NULL,
    musica_id INT NOT NULL,
    tipo_interacao tipo_interacao_enum NOT NULL,
    criado_em TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_usuario
        FOREIGN KEY(usuario_id)
        REFERENCES usuarios(usuario_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_musica_interacao
        FOREIGN KEY(musica_id)
        REFERENCES musicas(musica_id)
        ON DELETE CASCADE,
    PRIMARY KEY (usuario_id, musica_id)
);

CREATE OR REPLACE FUNCTION gatilho_definir_timestamp_atualizacao()
RETURNS TRIGGER AS $$
BEGIN
  NEW.atualizado_em = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS definir_timestamp_atualizacao ON interacoes_usuario_musica;
CREATE TRIGGER definir_timestamp_atualizacao
BEFORE UPDATE ON interacoes_usuario_musica
FOR EACH ROW
EXECUTE FUNCTION gatilho_definir_timestamp_atualizacao();

CREATE INDEX IF NOT EXISTS idx_musicas_titulo ON musicas (titulo);
CREATE INDEX IF NOT EXISTS idx_artistas_nome ON artistas (nome);
CREATE INDEX IF NOT EXISTS idx_playlists_nome ON playlists (nome);
CREATE INDEX IF NOT EXISTS idx_playlist_musicas_musica_id ON playlist_musicas (musica_id);
CREATE INDEX IF NOT EXISTS idx_interacoes_usuario_musica_musica_id ON interacoes_usuario_musica (musica_id);
