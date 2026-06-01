## Galyleo Service Overview

The Galyleo Service is the new, centralized hub for data and dashboards in  Galyleo Hub. It is the primary method for storing, sharing, and publishing all  Galyleo data tables and dashboards in a secure, collaborative environment.

### Built on an Open-Source Foundation

The service is built on the  foundation of the **Simple Data Transfer Protocol (SDTP)**, an open standard for querying and interacting with structured data. You can read the full SDTP specification [here](https://global-data-plane.github.io/sdtp).

While SDTP provides the core data querying capabilities, the Galyleo Service enhances it in four  ways:

### 1. Unified Management for Tables and Dashboards

The SDTP is a data transfer and data-querying protocol.  It is silent on data storage, sharing, and authentication, relying explicitly on implementation choices at hosting sites.  Further, SDTP's only data type is Simple Data Markup Language (SDML) tables.  
The Galyleo Service provides a system for storing both data tables and dashboards. It treats both data tables and dashboards as first-class citizens, allowing you to store and manage them in one central location.

### 2. Secure, Granular Sharing

A  per-user, per-object sharing architecture is built into the service. By default, all uploaded items are private to the user. The user can then securely share specific tables or dashboards with individual users, or with all users of the Galyleo Hub, or with the public at large (publication).

### 3. First-Class Dashboard Support

Beyond just data tables, the Galyleo Service is designed to store and serve  dashboard files. This allows users  to publish and share entire interactive visualizations, not just the underlying data.

### 4. An Intuitive Web UI

The service includes a  Web UI for managing data and dashboard  assets. Through the UI, users  easily upload, view, download, and manage sharing permissions for their tables and dashboards.