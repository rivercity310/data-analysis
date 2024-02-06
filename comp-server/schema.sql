CREATE TABLE users (
    user_id                 INT         NOT NULL,
    user_email              VARCHAR     NOT NULL,
    user_password           VARCHAR     NOT NULL,
    PRIMARY KEY (user_id)
)


CREATE TABLE product (
    product_id              INT         NOT NULL,
    product_name            VARCHAR     NOT NULL,
    product_architecture    VARCHAR     NOT NULL,
    register_user_id        INT         NOT NULL,
    PRIMARY KEY (product_id)
    FOREIGN KEY (register_user_id) REFERENCES users (user_id)
)


CREATE TABLE patch_detail (
    patch_detail_id         INT         NOT NULL,
    bulletin_id             VARCHAR     NOT NULL,
    bulletin_url            VARCHAR     NOT NULL,
    issue                   VARCHAR     NOT NULL,
    cve                     VARCHAR     NOT NULL,
    severity                VARCHAR     NOT NULL,
    patch_status            VARCHAR     NOT NULL,
    created_at              TIMESTAMP   NOT NULL,
    modified_at             TIMESTAMP   NOT NULL,
    ahnlab_created_at       TIMESTAMP   NOT NULL,
    ahnlab_modified_at      TIMESTAMP   NOT NULL,
    PRIMARY KEY (id)
)


CREATE TABLE patch (
    patch_id                INT         NOT NULL,
    patch_title             VARCHAR     NOT NULL,
    patch_summary           VARCHAR     NOT NULL,
    patch_language          VARCHAR     NOT NULL,
    patch_status            INT         NOT NULL,
    patch_detail_id         INT         NOT NULL,
    product_id              INT         NOT NULL,
    PRIMARY KEY (patch_id),
    FOREIGN KEY (patch_detail_id) REFERENCES patch_detail (patch_detail_id),
    FOREIGN KEY (product_id) REFERENCES product (product_id)
)

