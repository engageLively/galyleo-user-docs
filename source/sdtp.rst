What is SDML?
=============

**Simple Data Markup Language (SDML)** is a JSON-based format for representing structured tabular data. Each SDML document describes a single table, including:

- A ``type`` field (e.g., ``"RowTable"``, ``"RemoteTable"``).
- A ``schema`` defining column names and data types.
- A data source such as embedded rows, a file reference, or a remote URL.

SDML is human-readable, portable, and easy to integrate into data pipelines and web-based tools.

What is SDTP?
=============

**Simple Data Transfer Protocol (SDTP)** is a RESTful protocol for accessing SDML tables over HTTPS. It’s designed to be simple, scalable, and secure by building directly on the web’s existing infrastructure.

That's a crucial capability — it positions SDTP not just as a transport layer, but as a **query interface over data services**.

Key Features
------------

- **Web-native**: Tables are accessed via standard HTTP(S) endpoints — no special clients required.

- **Secure by design**: SDTP leverages all the built-in mechanisms of HTTPS (authentication, authorization, encryption, etc.) without inventing new ones.

- **Selective querying**: Instead of fetching entire tables, SDTP supports **at-source filtering and querying**, e.g.::

    GET /tables/nightingale?disease<10&wounds>25

  This conserves client bandwidth and makes it possible to:

  - Stream data from **infinitely large** or **dynamic** sources.
  - Support **computed or virtual tables**, whose content is generated on-demand.
  - Avoid pre-materializing large datasets on disk.

- **RESTful simplicity**: Each table is a resource, and all interactions follow standard web semantics (GET, POST, etc.).

In short, SDTP turns the web into a queryable, secure, and scalable data layer — no heavyweight database or custom server required.
