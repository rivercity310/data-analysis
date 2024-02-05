CREATE TABLE product (
    id                      INT         NOT NULL,
    product_name            VARCHAR     NOT NULL,
    product_architecture    VARCHAR     NOT NULL,
    PRIMARY KEY (id)
)


CREATE TABLE patch_detail (
    id                      INT         NOT NULL,
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
    id                      INT         NOT NULL,
    patch_title             VARCHAR     NOT NULL,
    patch_summary           VARCHAR     NOT NULL,
    patch_language          VARCHAR     NOT NULL,
    patch_status            INT         NOT NULL,
    patch_detail_id         INT         NOT NULL,
    product_id              INT         NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (patch_detail_id) REFERENCES patch_detail (id),
    FOREIGN KEY (product_id) REFERENCES product (id)
)

