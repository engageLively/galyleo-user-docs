# **Galyleo Hub Administrator's Guide**

## **1\. Introduction**

Welcome to the administrator's guide for Galyleo Hub. This guide provides a complete walkthrough for installing, configuring, and managing a Galyleo Hub instance on Google Cloud Platform (GCP).

Galyleo Hub is built upon the **Zero to JupyterHub with Kubernetes (Z2JH)** project. As such, this guide is a companion to the official [Z2JH Administrator's Guide](https://z2jh.jupyter.org/en/latest/administrator/index.html), which serves as the foundational reference. This document provides an end-to-end tutorial covering the GCP environment, Kubernetes setup, Galyleo-specific services, and operational procedures.

## **Part I: Environment Setup**

This section covers the initial setup of your Google Cloud environment and the required tools.

### **2\. Setting Up Your GCP Project**

For security and resource management, we recommend deploying each Galyleo Hub instance in its own dedicated GCP project.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).  
2. In the top menu bar, click the project selector and then click **"New Project"**.  
3. Give your project a descriptive name (e.g., galyleo-hub-production) and configure your organization and billing account.  
4. Once the project is created, make sure it is selected in the project selector.  
5. Enable the necessary APIs for your new project:  
   * Kubernetes Engine API  
   * Cloud Datastore API  
   * Google Secret Manager API  
   * Cloud Build API (if you plan to build container images)

### **3\. Required Tools (gcloud, kubectl, Helm)**

The easiest way to get all the necessary command-line tools is to use the **Google Cloud Shell**, which comes pre-installed with everything you need.

* **To open Cloud Shell:** Click the \[\>\_\] icon in the top-right corner of the Google Cloud Console.

If you prefer to work from your local machine, you will need to install:

1. **gcloud CLI:** The command-line tool for interacting with GCP. [Installation Guide](https://cloud.google.com/sdk/docs/install).  
2. **kubectl:** The command-line tool for interacting with Kubernetes clusters. You can install it via gcloud: gcloud components install kubectl.  
3. **Helm:** The package manager for Kubernetes. [Installation Guide](https://helm.sh/docs/intro/install/).  
4. **gsutil:** A tool for interacting with Google Cloud Storage. It is installed as part of the gcloud CLI.

A significant advantage of using Google Cloud shell is that all required GCP  libraries are pre-installed and the user is pre-authenticated to the Google Cloud platform.

### **4\. Creating a Service Account**

A dedicated service account is essential for granting permissions to the Galyleo Hub infrastructure securely.  A service account is an email address (e.g. [1024780277534-compute@developer.gserviceaccount.com](mailto:1024780277534-compute@developer.gserviceaccount.com))  to which permissions can be attached.  Service accounts authenticate with ssh keys, which can be created from the IAM page.

1. In the Cloud Console, navigate to **IAM & Admin \> Service Accounts**.  
2. Click **"Create Service Account"**.  
3. Give it a name (e.g., galyleo-hub-admin) and a description.  
4. **Grant the following IAM roles** to this service account. These permissions are required for the hub to manage its own infrastructure and for the Galyleo services to function correctly:  
   * **Kubernetes Engine Admin:** Allows creating and managing GKE clusters.  
   * **Compute Admin:** Allows the GKE control plane to create and manage Compute Engine nodes (VMs) for the cluster.  
   * **Service Account User:** Allows GKE nodes to run as this service account.  
   * **Storage Object Admin:** Grants full control over objects in the GCS bucket used for Galyleo data.  
   * **Cloud Datastore User:** Allows the Galyleo service to read from and write to the permissions database.  
   * **Artifact Registry Reader:** Allows the cluster to pull container images from Google Artifact Registry. (If building your own images, you may also need "Artifact Registry Writer").  
5. Create the service account. You do not need to create keys at this stage.

## **Part II: Infrastructure Provisioning**

This section covers the creation of the core infrastructure on GCP.

### **5\. Creating a GKE Cluster**

The Galyleo Hub runs on the Google Kubernetes Engine (GKE). You can create the cluster using the Cloud Console UI or via the gcloud command line. Using the command line is repeatable and recommended.

#### **5.1 Using the Cloud Console (UI)**

1. Navigate to **Kubernetes Engine \> Clusters**.  
2. Click **"Create"** and choose a **GKE Standard** cluster.  
3. **Cluster basics:** Give your cluster a name and select a region.  
4. **Node Pools:** This is critical for performance and cost.  
   * It is recommended to have at least two node pools:  
     * A default-pool for core JupyterHub services (Proxy, Hub, etc.). A small machine type like e2-standard-2 is often sufficient.  
     * A user-pool for the single-user notebook servers. Choose a machine type appropriate for your users' workloads (e.g., n2-standard-4 or larger). Enable cluster autoscaling on this pool.  
5. **Networking:** Ensure the cluster has access to the internet to pull container images.  
6. **Security:** Under "Security," select the service account you created in the previous step.

#### **5.2 Using the gcloud Command Line**

Replace the placeholder values in the following script to create your cluster. This script creates a cluster with two separate node pools as recommended.

```

# Set variables for your configuration
export PROJECT_ID="your-gcp-project-id"
export CLUSTER_NAME="galyleo-hub-cluster"
export REGION="us-central1"
export SERVICE_ACCOUNT_EMAIL="galyleo-hub-admin@${PROJECT_ID}.iam.gserviceaccount.com"

# Set your project context
gcloud config set project $PROJECT_ID

# --- Create the GKE Cluster with the core services node pool ---
gcloud container clusters create $CLUSTER_NAME \
  --region $REGION \
  --machine-type "e2-standard-2" \
  --num-nodes "1" \
  --node-locations "${REGION}-a,${REGION}-b" \
  --service-account $SERVICE_ACCOUNT_EMAIL \
  --scopes "[https://www.googleapis.com/auth/cloud-platform](https://www.googleapis.com/auth/cloud-platform)"

# Connect kubectl to the new cluster
gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION

# --- Add a dedicated node pool for user notebooks with autoscaling ---
gcloud container node-pools create "user-pool" \
  --cluster $CLUSTER_NAME \
  --region $REGION \
  --machine-type "n2-standard-4" \
  --num-nodes "0" \
  --enable-autoscaling \
  --min-nodes "0" \
  --max-nodes "10" \
  --service-account $SERVICE_ACCOUNT_EMAIL \
  --scopes "[https://www.googleapis.com/auth/cloud-platform](https://www.googleapis.com/auth/cloud-platform)"

```

### **6\. Creating a Kubernetes Namespace**


Before you can deploy the hub, you need to connect your command-line tools to your new cluster and create a dedicated workspace for the hub's components.

#### **6.1 Connecting kubectl to your GKE Cluster**

After your GKE cluster has been created, your local kubectl command-line tool needs to be configured with the correct credentials and endpoint to communicate with it. The gcloud tool makes this simple.

Run the following command, replacing the variables with your cluster's name and region:

```

# Set variables for your configuration
export CLUSTER_NAME="galyleo-hub-cluster"
export REGION="us-central1"

# This command fetches credentials for your cluster and configures kubectl
gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION

```

You can verify the connection by asking kubectl to list the nodes in your cluster:

```

kubectl get nodes

```

You should see the nodes from the pools you created earlier.

#### **6.2 What is a Kubernetes Namespace?**

A Kubernetes namespace provides a way to create a virtual cluster inside your physical cluster. Think of it like creating separate, walled-off offices inside a large building. Each namespace can have its own resources (applications, services, secrets) and policies.

Using a dedicated namespace for your Galyleo Hub is a critical best practice for several reasons:

* **Isolation:** It keeps all the components of your hub (the proxy, the hub itself, user notebooks, the Galyleo service) logically separate from any other applications you might run on the same cluster.  
* **Avoiding Naming Conflicts:** Resources within one namespace can have the same names as resources in another without conflicting.  
* **Resource Management:** You can set resource quotas (CPU, memory) on a per-namespace basis.  
* **Scoped Permissions:** You can grant administrative permissions to a user for just a single namespace, without giving them control over the entire cluster.

#### **6.3 Creating the galyleo-hub Namespace**

We will create a single namespace called galyleo-hub to contain all the components of our deployment.

```

kubectl create namespace galyleo-hub

```

From this point forward, almost every kubectl and helm command you run should include the \--namespace galyleo-hub flag to ensure you are working within this isolated environment.  If the \--namespace galyleo-hub flag is omitted, the commands will be on the default namespace.  To set the default namespace to galyleo-hub, run the following command:

```

kubectl config set-context --current --namespace=galyleo-hub
```

### **7\. Setting up a GCS Bucket**

The Galyleo Service requires a Google Cloud Storage (GCS) bucket to act as the central, persistent repository for all Galyleo tables (`.sdml` files) and dashboards (`.gd.json` files).

#### **7.1 What is a Google Cloud Storage Bucket?**

Google Cloud Storage is a high-performance, durable, and massively scalable object storage service. Think of a **bucket** as the primary container that holds your data, much like a top-level folder in a file system. Unlike a traditional file system, however, GCS offers enterprise-grade features that make it ideal for cloud applications:

* **High Performance:** GCS is optimized for fast read and write operations, which is critical for loading and saving the datasets and dashboards used by Galyleo.  
* **Security:** All data uploaded to GCS is automatically encrypted at rest, with no additional setup required. Access is controlled by granular IAM permissions.  
* **Durability and Availability:** Data is stored redundantly across multiple locations to protect against hardware failure and ensure it's accessible when needed.  
* **Excellent Tooling:** GCS is supported by powerful command-line tools like `gsutil` for administration and robust libraries like `gcsfs` for seamless access from Python environments like Jupyter notebooks.

#### **7.2 Best Practices for Galyleo**

* **Location:** For production hubs, it is best practice to use a **multi-region** bucket. This provides the highest availability by storing your data in geographically separate locations.  
* **Access Control:** **Never** make the storage bucket public. The Galyleo Hub is designed to act as a secure gateway, managing all reads and writes programmatically. You must enforce public access prevention.

#### **7.3 Creating the Storage Bucket**

You can create the bucket using either the web-based Cloud Console or the `gsutil` command line.

**Using the Cloud Console (UI)**

1. In the Google Cloud Console, navigate to **Cloud Storage \> Buckets**.  
2. Click **"Create Bucket"**.  
3. **Name your bucket:** Give it a globally unique name. This name will be used for your `GALYLEO_STORAGE_BUCKET` environment variable.  
4. **Choose where to store your data:** Select a **Multi-region** location for the best availability.  
5. **Choose a storage class:** **Standard** is the correct choice for frequently accessed data.  
6. **Choose how to control access to objects:** Select **Uniform**.  
7. **Choose how to protect object data:** Leave the defaults.  
8. **Prevent public access:** This is the most critical step. Ensure the box for **"Enforce public access prevention on this bucket"** is **checked**.  
9. Click **"Create"**.

**Using the `gsutil` Command Line**

The `gsutil` tool provides a simple command for creating buckets.

```
# Set variables for your configuratio
export PROJECT_ID="your-gcp-project-id"
export BUCKET_NAME="your-globally-unique-bucket-name" # e.g., galyleo-hub-storage-prod
export LOCATION="US" # Example multi-region
# Create the bucket with recommended settings
gsutil mb -p $PROJECT_ID -l $LOCATION -b on gs://$BUCKET_NAME/
# Enforce public access prevention
gsutil publicaccessblock set on gs://$BUCKET_NAME/
```

### **8\. Setting up the Cloud Datastore**

The Galyleo Service uses Google Cloud Datastore to manage a simple but critical piece of data: the access permissions for every table and dashboard.

#### **8.1 What is Google Cloud Datastore?**

Google Cloud Datastore is a highly scalable, fully managed NoSQL database. Unlike a traditional SQL database with rigid tables and columns, a NoSQL database stores data in a more flexible format, making it ideal for applications that need to evolve and scale easily.

Datastore is an excellent choice for Galyleo's permissions system because:

* **It's Schemaless:** We can store our simple permissions data without defining a rigid structure. If we need to add more information later, we can do so without complex database migrations.  
* **It's Fast for Key-Based Lookups:** The primary way Galyleo checks permissions is by looking up an object's unique reference key. Datastore is optimized for exactly this kind of fast, direct lookup.  
* **It Scales Automatically:** As your hub grows with more users and objects, Datastore handles the scaling in the background with no administrative overhead.

#### **8.2 Datastore Concepts for Galyleo**

Datastore has a simple hierarchy that we use to keep permissions organized and secure.

* **Database:** A single project has a single Datastore database. The name of this database is your GCP Project ID.  
* **Namespace:** Within that database, you can create **namespaces** to partition your data. This is how we achieve multi-tenancy. **Each Galyleo Hub instance must have its own unique namespace.** This ensures the permissions for a development hub can never interfere with a production hub, even if they are in the same project. The service uses the `GALYLEO_PERMISSIONS_NAMESPACE` environment variable to select the correct namespace.  
* **Entity & Kind:** An **entity** is the fundamental unit of storage, similar to a row in a SQL table. Each entity is of a certain **kind**, which is like the table name. For simplicity, Galyleo stores all permissions under a single kind: `"key"`.  
* **Key:** Each entity has a unique **key**. For Galyleo, the key is the object's unique three-part reference string: `<object-type>/<owner-email>/<object-name>`.  
* **Properties:** Each entity contains **properties**, which are the data values. We use a single property that holds a list of user emails who are permitted to access the object.

#### **8.3 Creating the Datastore Database**

Setting up the database is a one-time operation for your GCP project.

**Using the Cloud Console (UI)**

1. In the Google Cloud Console, navigate to the **Datastore** section (you can use the search bar at the top).  
2. If this is the first time you've used Datastore in this project, you will be prompted to select a database mode. Choose **Native Mode**.  
3. Next, you will be prompted to select a **location** for your database. This location cannot be changed later. Choose a location that is geographically close to your users and your GKE cluster.  
4. Click **"Create Database"**. The provisioning process can take a few minutes.

Once the database is active, you are done. The Galyleo Service will automatically create the namespace specified in your configuration on its first connection.

**Using the `gcloud` Command Line**

While the initial database creation is typically done via the UI, you can ensure the necessary API is enabled using `gcloud`.

```
# Set your project ID
export PROJECT_ID="your-gcp-project-id"
# Enable the Cloud Datastore API for your project
gcloud services enable datastore.googleapis.com --project=$PROJECT_ID
```

### **9\. Setting up DNS and Google OAuth**

To make your Galyleo Hub accessible to users with a professional, easy-to-remember URL (e.g., `galyleo.your-company.com`) and to secure it with Google-based login, you need to configure three components: a static IP address, a DNS record, and Google OAuth credentials.

#### **9.1 Reserving a Static IP Address**

**What is a Static IP Address?**

By default, cloud resources are often assigned *ephemeral* IP addresses, which can change if the resource is stopped and restarted. For a public-facing service like a JupyterHub, you need a permanent, unchanging address. A **static IP address** is an address that you reserve in your project and that remains yours until you explicitly release it.

**Why is it necessary?**

The Domain Name System (DNS) works by pointing a hostname to a specific IP address. If that IP address changes, your URL will break. Reserving a static IP gives you a stable target for your DNS record.

**Using the Cloud Console (UI)**

1. In the Google Cloud Console, navigate to **VPC Network \> IP Addresses**.  
2. Click **"Reserve External Static IP Address"**.  
3. Give the address a **Name** (e.g., `galyleo-hub-prod-ip`).  
4. Choose the **Region** where you created your GKE cluster.  
5. Click **"Reserve"**.  
6. Take note of the IP address that is allocated.

**Using the `gcloud` Command Line**

```
# Set variables for your configuration
export IP_ADDRESS_NAME="galyleo-hub-prod-ip"
export REGION="us-central1"
# Reserve the static IP address
gcloud compute addresses create $IP_ADDRESS_NAME --region=$REGION
# View the reserved IP address
gcloud compute addresses describe $IP_ADDRESS_NAME --region=$REGION --format='value(address)'
```

#### **9.2 Configuring DNS**

**What is DNS?**

DNS (Domain Name System) is the phonebook of the internet. It translates human-friendly domain names (like `www.google.com`) into the IP addresses that computers use to connect to each other.

**Why is it necessary?**

You need to create a DNS record to point your desired hostname (e.g., `galyleo.your-company.com`) to the static IP address you reserved in the previous step.

**Creating an A Record**

This step is performed in your **domain registrar's** control panel (e.g., Google Domains, GoDaddy, Cloudflare).

1. Log in to your domain registrar and navigate to the DNS management page for your domain.  
2. Create a new DNS record with the following settings:  
   * **Type:** `A`  
   * **Host** or **Name:** The subdomain you want to use (e.g., `galyleo` for `galyleo.your-company.com`).  
   * **Value** or **Points to:** The static IP address you reserved.  
   * **TTL (Time To Live):** You can typically leave this at the default (e.g., 1 hour).  
3. Save the record. Note that it can take anywhere from a few minutes to several hours for DNS changes to propagate across the internet.

   #### **9.3 Creating Google OAuth Credentials**

**What is OAuth?**

OAuth is a secure authorization standard that allows users to log in to an application (like Galyleo Hub) using their existing Google account, without ever sharing their Google password with the application.

**Why is it necessary?**

JupyterHub uses OAuth as its primary authentication mechanism, ensuring that only authorized users from your organization can access the hub.

**Creating an OAuth Client ID**

1. In the Google Cloud Console, navigate to **APIs & Services \> Credentials**.  
2. Click **"Create Credentials"** and select **"OAuth client ID"**.  
3. If prompted, you may need to configure an "OAuth consent screen" first. Fill out the required information for your organization.  
4. For **Application type**, select **"Web application"**.  
5. Give it a **Name** (e.g., "Galyleo Hub Production").  
6. Under **"Authorized redirect URIs"**, click **"Add URI"**. This is a critical step. The URI must be your hub's domain followed by `/hub/oauth_callback`.  
   * Example: `https://galyleo.your-company.com/hub/oauth_callback`  
7. Click **"Create"**.  
8. A window will pop up showing your **Client ID** and **Client Secret**. **Copy both of these values immediately and store them securely.** You will need them for your `config.yaml` file, and you cannot view the secret again after closing this window.

   

## **Part III: Hub Configuration & Deployment**

### **10\. Hub Configuration and Deployment**

With the cloud infrastructure in place, the next step is to configure and deploy the JupyterHub software itself. This is managed using a tool called Helm.

#### **10.1 Understanding Helm**

**Helm** is often called "the package manager for Kubernetes." It's a tool that simplifies deploying and managing complex applications on a Kubernetes cluster.

* **Chart:** A Helm **chart** is a collection of files that describe a related set of Kubernetes resources. Think of it as an installation package, like an `.rpm` or `.deb` file in Linux. It contains templates for all the necessary components (deployments, services, etc.) needed to run an application.  
* **Release:** A **release** is a specific instance of a chart running in your cluster. You can install the same chart multiple times, and each one is a separate release.  
* **Values:** A chart is a template. The specific configuration details are provided in a **values** file. For JupyterHub, this is our `config.yaml` file. It allows you to customize the deployment without ever modifying the chart's source code.

#### **10.2 The JupyterHub Helm Chart**

We don't build JupyterHub from scratch. We use the official, community-maintained Helm chart, which is the standard for deploying JupyterHub on Kubernetes. You can find the chart and its extensive documentation here:

* **JupyterHub Helm Chart Repository:** [https://jupyterhub.github.io/helm-chart/](https://jupyterhub.github.io/helm-chart/)

#### **10.3 Customizing the Galyleo Hub**

The power of the Helm chart is that it allows for deep customization. The Galyleo Hub is a specialized version of the standard JupyterHub, and we configure it in two primary ways:

1. **`config.yaml`:** This is the main file where we define all our settings. This includes everything from the domain name and OAuth credentials to the specific Docker images available to users and the resources (CPU, memory) they are allocated. We will walk through the Galyleo Hub's `config.yaml` in the following sections.  
2. **Custom Python Code (`galyleo_hub.py`):** For more advanced customizations that can't be expressed in YAML, the Helm chart allows us to inject custom Python code directly into the Hub's configuration. We use this to implement the `GalyleoSpawner`, which provides a seamless experience for users accessing the Galyleo service from their notebooks.

### **11\. The Galyleo Hub config.yaml File**

The config.yaml file is the heart of your JupyterHub deployment. It's a single file where you define all the settings, secrets, and custom behaviors that make your hub unique. In this section, we will walk through the config.yaml used for the Galyleo Hub, explaining what each section does.

#### **11.1 The Full config.yaml Template**

Below is the complete, annotated config.yaml file. You should create a copy of this, name it config.yaml, and fill in the required secret values.

```

# config.yaml - Galyleo Hub Configuration
# -----------------------------------------

# proxy: Configures the public-facing entry point of the Hub.
proxy:  
  # A secret token to secure communication between the Hub and the proxy.
  # Generate with: openssl rand -hex 32
  secretToken: "" 
  
  # Configures HTTPS for the hub.
  https:
    enabled: true
    # The public hostname(s) of your hub.
    hosts:
      - "galyleo-beta.engagelively.com"
    # Uses Let's Encrypt to automatically provision a free SSL certificate.
    letsencrypt:
      contactEmail: info@engagelively.com

# hub: Core configuration for the JupyterHub application itself.
hub:
  # A secret key for signing browser cookies.
  # Generate with: openssl rand -hex 32
  cookieSecret: ""
  
  # extraConfig allows us to inject custom Python code into the Hub's configuration.
  # This is how we add Galyleo's unique features.
  extraConfig: 
    # Generic settings for the underlying web server.
    myConfig: |
      c.JupyterHub.tornado_settings = { 'headers': {'Content-Security-Policy': "frame-ancestors https://*.engagelively.com "}}
      c.LabApp.user_settings_dir = '/usr/local/jupyter/.jupyter/lab/user-settings'
    
    # This block loads our custom galyleo_hub.py script and runs the setup
    # function to register the Galyleo service with the Hub.
    10-galyleo-config: |
      import sys
      sys.path.insert(0, '/etc/jupyterhub/custom')
      from galyleo_hub import setup_galyleo_service
      
      # This token must match the GALYLEO_SERVICE_API_TOKEN in the service deployment.
      galyleo_api_token = '' 
      cluster_url = '[https://galyleo-beta.engagelively.com](https://galyleo-beta.engagelively.com)'
      namespace = 'jh2-test'
      setup_galyleo_service(c, cluster_url, namespace, galyleo_api_token)
      
    # This block defines our custom GalyleoSpawner. Its job is to generate a
    # user-specific API token and inject it as an environment variable into
    # the user's notebook server when it starts.
    11-galyleo-spawner_config: |
      # [Full Python code for the GalyleoSpawner is omitted for brevity, 
      #  it is sourced from the galyleo_hub.py file]
      from kubespawner import KubeSpawner
      from traitlets import Unicode
      # ... GalyleoSpawner class definition ...
      c.JupyterHub.spawner_class = GalyleoSpawner
      
  # Configures the Google OAuth authenticator.
  config:
    GoogleOAuthenticator:
      # Your OAuth Client ID from the Google Cloud Console.
      client_id: "" 
      # Your OAuth Client Secret from the Google Cloud Console.
      client_secret: "" 
      # The redirect URL you configured in your OAuth credentials.
      oauth_callback_url: "[https://galyleo-beta.engagelively.com/hub/oauth_callback](https://galyleo-beta.engagelively.com/hub/oauth_callback)"
      
    Authenticator:
      # A list of Google accounts that will have admin privileges.
      admin_users: 
        - user1@example.com       
        - user2@example.com
      # A list of all Google accounts that are allowed to log in.
      allowed_users:        
        - user1@example.com        
        - user2@example.com
	# --- THIS IS THE KEY ---
# Allows admins to add new users via the web UI after the hub has started.
allow_existing_users: true
# cull: Configures the idle notebook culler.
cull:
  # If true, the culler service is enabled.
  enabled: true
  # Timeout in seconds after which an idle server is shut down.
  timeout: 3600
  # How often, in seconds, to check for idle servers.
  every: 300

# singleuser: Configures the environment for each user's notebook server.
singleuser:
  # The default URL the user is redirected to after their server starts.
  defaultUrl: "/lab"
  
  # Configures the persistent storage volume for each user.
  storage:
    capacity: 25G
    
  # Default resource limits for each user pod.
  memory:
    limit: 2G
    guarantee: 100M
  cpu:
    limit: 0.97
    guarantee: 0.002
    
  # A list of selectable environments (Docker images) for users.
  profileList:
    - display_name: "SciPy"
      description: "Scientific Python with Galyleo"
      kubespawner_override: 
        image: rickmcgeer/el-jupyter:scipy_0.0.9
    - display_name: "Data Science"
      description: "Data Science libraries with Galyleo"
      kubespawner_override: 
        image: rickmcgeer/el-jupyter:datascience_0.0.9
    - display_name: "Tensorflow"
      description: "Tensorflow with Galyleo"
      kubespawner_override: 
        image: rickmcgeer/el-jupyter:tensorflow_0.0.9

```

#### **11.2 Configuration Walkthrough**

**`proxy`**: This section configures the public-facing component of JupyterHub. It sets up automatic HTTPS using Let's Encrypt for the specified `hosts` and uses `secretToken` to secure internal communications.

**`hub`**: This is the core of the configuration.

* `cookieSecret`: A secret key used to secure browser session cookies.  
* `extraConfig`: This is a powerful feature of the Helm chart that allows us to inject raw Python configuration. We use it to load our custom `galyleo_hub.py` script. This script defines the `GalyleoAuthenticator` (to manage user groups) and the `GalyleoSpawner` (to inject API tokens for the Galyleo service). This is the key mechanism for extending the base JupyterHub with Galyleo's features.  
* `config`: This block configures the `GoogleOAuthenticator`.  
  * `GoogleOAuthenticator`: You must paste your `client_id` and `client_secret` here.  
  * `Authenticator`: This subsection controls user access.  
    * `admin_users`: Defines which users have administrative rights.  
    * `allowed_users`: A whitelist of users who can log in when the hub first starts.  
    * **`allow_existing_users: true`**: This is a crucial setting. It permits any user who has been manually added to the Hub's database via the admin panel to log in, even if they are not in the initial `allowed_users` list. This is what enables dynamic user management without restarting the hub.  
* **`cull`**: This section enables and configures the `jupyterhub-idle-culler`, a service that automatically shuts down user notebook servers after they've been idle for a specified period (`timeout`). This is essential for managing resource costs in a cloud environment.  
* **`singleuser`**: This section defines the environment for the individual user notebook servers.  
* `storage`, `memory`, `cpu`: These set the default persistent storage size and resource limits for each user.  
* `profileList`: This creates a dropdown menu on the spawner page, allowing users to select from different environments.


### **12\. The Galyleo Service YAML File**

The Galyleo Service is the backend that manages all tables and dashboards. It runs as a separate deployment within the same Kubernetes namespace as the JupyterHub. This allows it to communicate with the Hub for authentication while handling all the storage and permissions logic.

Below is an annotated walkthrough of the galyleo-service.yaml file used to deploy the service.

#### **12.1 The Full galyleo-service.yaml Template**

You will create a file named galyleo-service.yaml and populate it with the following content, filling in your specific secret values.

```

# galyleo-service.yaml
# Deploys the Galyleo backend service.

apiVersion: apps/v1
kind: Deployment
metadata:
  name: galyleo-service
  namespace: jh2-test # Must match your Hub's namespace
  
spec:
  replicas: 1
  selector:
    matchLabels:
      app: galyleo-service
  template:
    metadata:
      labels:
        app: galyleo-service
    spec:
      containers:
        - name: galyleo-service
          image: rickmcgeer/galyleo_service_platform:latest
          volumeMounts:
            - name: keys-secret
              mountPath: /app/.keys
              readOnly: true
          ports:
            - containerPort: 5000
          env:
              # --- Service Account Credentials ---
              - name: GOOGLE_APPLICATION_CREDENTIALS
                value: "/app/.keys/your-service-account-key.json"

              # --- Hub Integration ---
              - name: JUPYTER_HUB_API_TOKEN
                value: "" # An admin API token generated from the Hub UI
              - name: JUPYTERHUB_API_URL
                value: "https://<your-hub-domain>/hub/api"
              - name: GALYLEO_SERVICE_API_TOKEN
                value: "" # Must match 'galyleo_api_token' in config.yaml
              - name: GALYLEO_SECRET_KEY
                value: "" # Must match 'cookieSecret' in config.yaml

              # --- GCP Project and Service Info ---
              - name: GOOGLE_PROJECT
                value: "your-gcp-project-id"
              - name: BUCKET_NAME
                value: "your-galyleo-storage-bucket-name"
              - name: GALYLEO_PERMISSIONS_DATABASE
                value: "your-gcp-project-id" # Typically the project ID
              - name: GALYLEO_PERMISSIONS_NAMESPACE
                value: "galyleo-server" # The namespace you chose
              - name: GALYLEO_PORT
                value: "5000"

              # --- OAuth and Internal Service Configuration ---
              - name: GALYLEO_CLIENT_ID
                value: "service-galyleo"
              - name: GALYLEO_ROOT_URL
                value: "http://localhost/services/galyleo"
      volumes:
        - name: keys-secret
          secret:
            secretName: galyleo-keys # The Kubernetes secret holding your service account key
---
# Exposes the deployment as a network service within the cluster.
apiVersion: v1
kind: Service
metadata:
  name: galyleo-service
  namespace: jh2-test # Must match your Hub's namespace
spec:
  selector:
    app: galyleo-service
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000

```

#### **12.2 Configuration Walkthrough**

The galyleo-service.yaml file defines two Kubernetes objects: a **Deployment** and a **Service**.

* **Deployment**: This tells Kubernetes how to run the Galyleo Service application, including which Docker image to use, how many replicas to run, and, most importantly, what environment variables to set.  
* **Service**: This creates a stable internal network endpoint for the deployment. This is how the JupyterHub (and other components inside the cluster) can reliably find and talk to the Galyleo Service.

The most critical part of this file is the env section, which configures the service:

* **GOOGLE\_APPLICATION\_CREDENTIALS**: The path to the GCP service account key file, which must be mounted into the container from a Kubernetes secret. This gives the service its identity and permissions on Google Cloud.  
* **JUPYTER\_HUB\_API\_TOKEN**: An API token with admin privileges, which you must generate from the JupyterHub admin panel. This allows the Galyleo Service to query the Hub for user information.  
* **JUPYTERHUB\_API\_URL**: The public API URL for your JupyterHub.  
* **GALYLEO\_SERVICE\_API\_TOKEN**: A secret token used to authorize communication *from* the Hub *to* the Galyleo Service. This value **must exactly match** the galyleo\_api\_token you set in the Hub's config.yaml.  
* **GALYLEO\_SECRET\_KEY**: A secret key for signing its own tokens and sessions. This value **must exactly match** the cookieSecret you set in the Hub's config.yaml.  
* **BUCKET\_NAME**, **GALYLEO\_PERMISSIONS\_DATABASE**, **GALYLEO\_PERMISSIONS\_NAMESPACE**: These variables tell the service which GCS bucket and Datastore database/namespace to use for storage and permissions. They must match the resources you created in the earlier setup steps.

```

```

### **13\. Managing Secrets**

A secure deployment requires managing sensitive information—API tokens, secret keys, and service account credentials—without exposing them in your configuration files. Storing secrets directly in config.yaml or version control is a major security risk. This section outlines the best practices for managing secrets using Google Secret Manager and Kubernetes Secrets.

#### **13.1 The Problem: Plaintext Secrets**

Your config.yaml and galyleo-service.yaml files require several pieces of sensitive information to function. If you paste these values directly into the files and commit them to a Git repository, anyone with access to that repository can compromise your entire system.

#### **13.2 The Solution: Google Secret Manager**

 The recommended solution is to use Google Secret Manager, a centralized and secure vault for storing and managing sensitive data.

 **How it Works:** Secret Manager stores your secrets (like API tokens) as named objects. Each secret can have multiple versions, allowing you to rotate keys without downtime. Access to these secrets is tightly controlled by GCP's IAM permissions. Your service accounts need the "Secret Manager Secret Accessor" role to read them.

#### **13.3 Secrets Required for Galyleo Hub**

 You will need to create the following secrets for a complete deployment:

 For the Hub (config.yaml):

*  proxy-secret-token: The value for proxy.secretToken.

*  hub-cookie-secret: The value for hub.cookieSecret.

*  google-oauth-client-id: The value for hub.config.GoogleOAuthenticator.client\_id.

*  google-oauth-client-secret: The value for hub.config.GoogleOAuthenticator.client\_secret.

*  galyleo-service-api-token: The value for hub.extraConfig.10-galyleo-config.galyleo\_api\_token.

 For the Galyleo Service (galyleo-service.yaml):

*  jupyterhub-api-token: The admin token you generate from the Hub UI.

*  gcp-service-account-key: The entire JSON key file for your service account.

#### **13.4 Using Secrets in Kubernetes**

 There are two primary methods for making secrets from Secret Manager available to your applications running in Kubernetes:

 1\. Mounting Secrets as Files (Best for Files)

 This is the ideal method for the gcp-service-account-key. The process is:

1.  Store the JSON key file content as a secret in Secret Manager.

2.  Create a Kubernetes Secret object that pulls the value from Secret Manager.

3.  Mount that Kubernetes Secret as a volume into your container.

 The galyleo-service.yaml already uses this pattern:

```

     volumeMounts:
        - name: keys-secret
          mountPath: /app/.keys
          readOnly: true
...
      volumes:
        - name: keys-secret
          secret:
            secretName: galyleo-keys

```

 You would create the galyleo-keys Kubernetes secret, which securely holds your service account key file.

 2\. Injecting Secrets as Environment Variables (Best for Tokens)

 This is the best method for all the other individual token and key values. You store the token in Secret Manager, and your Kubernetes deployment YAML references it, injecting the value into an environment variable at runtime. This prevents the secret from ever being written to disk inside the container.

#### 13.5 Step-by-Step Instructions

 1\. Create the Secrets in Google Secret Manager:

 For each secret string (like your proxy token), run the following commands in the Cloud Shell:

```

# Create the secret container
gcloud secrets create proxy-secret-token

# Add the secret value as the first version
# (Generate the actual value using openssl rand -hex 32)
echo "YOUR_GENERATED_PROXY_TOKEN" | gcloud secrets versions add proxy-secret-token --data-file=-

```

 Repeat this process for all the required secret strings.

 2\. Give Your Service Account Access:

 Your GKE nodes' service account needs permission to access these secrets.

```

gcloud secrets add-iam-policy-binding proxy-secret-token \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL" \
  --role="roles/secretmanager.secretAccessor"

```

 3\. Reference the Secrets in Your Deployments:

 How you reference the secrets depends on whether you are using Helm (config.yaml) or a standard Kubernetes deployment (galyleo-service.yaml). The principle is to reference the secret by name rather than including its value. Your deployment manifests will contain instructions to fetch the secret's value directly from the secret store when the container starts.

### **14\. Deploying the Hub and Service**

Once all the prerequisite cloud resources are created and your configuration files are complete, you are ready to deploy the Galyleo Hub. This section walks through the commands in the `start-full.sh` script, explaining what each one does.

#### **14.1 Deployment Prerequisites**

Before running the script, ensure you are in a directory containing the following files:

* `config.yaml` (with all secrets filled in)  
* `galyleo-service.yaml` (with all secrets filled in)  
* `galyleo_hub.py`  
* Your GCP service account key file (e.g., `your-service-account-key.json`)

You must also have the `jupyterhub/jupyterhub` Helm chart added to your local Helm repository. If you haven't done so, run:

```
helm repo add jupyterhub [https://jupyterhub.github.io/helm-chart/](https://jupyterhub.github.io/helm-chart/)
helm repo update

```

#### **14.2 The `start-full.sh` Script**

The deployment is a two-stage process: first, we deploy the JupyterHub using Helm, and second, we deploy the Galyleo Service using `kubectl`.

```
#!/bin/bash

# Define a variable for your namespace to avoid repetition
NAMESPACE="jhub-kct-free"

# --- Step 1: Create the Kubernetes Namespace ---
kubectl create namespace $NAMESPACE

# --- Step 2: Create the Kubernetes Secret for the Service Account ---
kubectl create secret generic galyleo-keys --from-file=/path/to/your-service-account-key.json -n $NAMESPACE

# --- Step 3: Create a ConfigMap for our custom Python code ---
kubectl create configmap galyleo-hub-config --from-file=galyleo_hub.py -n $NAMESPACE

# --- Step 4: Deploy JupyterHub using Helm ---
helm upgrade --cleanup-on-fail \
  --install jhub \
  jupyterhub/jupyterhub \
  --namespace $NAMESPACE \
  --values config.yaml

# --- Step 5: Deploy the Galyleo Service ---
kubectl apply -f galyleo-service.yaml --namespace=$NAMESPACE

```

#### **14.3 Command-by-Command Explanation**

1. **`kubectl create namespace $NAMESPACE`**  
   * This creates the dedicated Kubernetes namespace where all components of your hub will live. This isolates your deployment from other applications running in the cluster.  
2. **`kubectl create secret generic galyleo-keys ...`**  
   * This command takes your GCP service account JSON key file from your local machine and stores it as a secure `Secret` object within your Kubernetes namespace. This is what allows the Galyleo Service to securely access its credentials without them being in the deployment file.  
3. **`kubectl create configmap galyleo-hub-config ...`**  
   * This takes your custom `galyleo_hub.py` file and stores it as a `ConfigMap`. The JupyterHub Helm chart is configured to automatically mount the contents of a ConfigMap named `galyleo-hub-config` into the Hub container at `/etc/jupyterhub/custom`, making our custom code available to the Hub at runtime.  
4. **`helm upgrade --install ...`**  
   * This is the main command that deploys JupyterHub.  
     * `helm upgrade --install`: This is an "upsert" command. It will install the chart if it's not already present, or upgrade it if it is. This makes the script safe to re-run.  
     * `jhub`: This is the *release name* for your deployment.  
     * `jupyterhub/jupyterhub`: The name of the chart we are deploying.  
     * `--namespace $NAMESPACE`: Specifies which namespace to deploy into.  
     * `--values config.yaml`: This is the most important flag. It tells Helm to use our `config.yaml` file to override all the default settings in the chart.  
5. **`kubectl apply -f galyleo-service.yaml ...`**  
   * After the Hub is deployed, this command deploys the Galyleo Service. `kubectl apply` reads the `galyleo-service.yaml` file and creates the Deployment and Service objects it defines within your namespace.

   

```

```

## **Part IV: Operations and Maintenance**

### **14\. Checking Status with kubectl**

These commands are essential for monitoring your hub's health.

* **View all running components (pods):**

```

kubectl get pods --namespace galyleo-hub

```

    
  (Look for a hub, proxy, galyleo, and user- pods. Their status should be Running.)

* **View services (like the proxy's load balancer):**

```

kubectl get services --namespace galyleo-hub

```

### **15\. Checking Logs**

If a pod is crashing or misbehaving, its logs are the first place to look.

* **Get logs for the main hub pod:**

```

kubectl logs deployment/hub --namespace galyleo-hub

```

*   
  **Get logs for the Galyleo service:**

```

kubectl logs deployment/galyleo --namespace galyleo-hub

```

*   
  **To follow logs in real-time, add the \-f flag.**

### **16\. Restarting in Case of an Error**

If you've applied a new configuration and a component is stuck, you can force a restart.

* **Restart the Hub and user pods:**

```

kubectl rollout restart deployment/hub --namespace galyleo-hub

```

*   
  **Restart the Galyleo service:**

```
kubectl rollout restart deployment/galyleo --namespace galyleo-hub

```

User management in a Galyleo-enabled Zero to JupyterHub (Z2JH) deployment is primarily handled through the config.yaml file, with real-time administration available through the JupyterHub Admin dashboard.

### **16\.Authorizing Users to Log In**

For authenticators like Google or GitHub, users are not "added" manually. Instead, they are *authorized* to log in by adding their usernames (or email addresses) to a specific list in your config.yaml.

#### **16.1 The allowed\_users List**

To grant a user permission to log into the Hub, add their identifier to the allowed\_users list under the Authenticator configuration.

```

# In your config.yaml
hub:
  config:
    Authenticator:
      allowed_users:        
        - user-one@example.com        
        - user-two@example.com

```

### **16.2 The allow\_existing\_users Flag**

The special flag allow\_existing\_users: true is also set. This tells the authenticator that it should allow any user who *already exists* in the JupyterHub database to log in. This is useful in advanced scenarios but for most cases, managing the allowed\_users list is the primary method of controlling access.

### **17\. Granting Admin Privileges**

You can grant administrative privileges to trusted users by adding them to the admin\_users list in config.yaml. Administrators have access to the Admin Panel and can manage other users and their servers.

```

# In your config.yaml
hub:
  config:
    Authenticator:
      admin_users: 
        - your-admin@example.com

```

### **18\. Troubleshooting**

When a complex system like a Galyleo-enabled JupyterHub encounters issues, a methodical approach to debugging is key. This guide covers the most common failure scenarios and how to diagnose them using standard Kubernetes tools.

The primary tool in your arsenal will always be kubectl, specifically the commands kubectl get pods, kubectl describe pod, and kubectl logs.

####  **18.1 Scenario 1: Pods Are Not Starting Correctly**

If user servers are not spawning or the Hub itself is unavailable, the first step is to check the status of the pods in your namespace.

```

kubectl get pods -n your-namespace

```

Look for any pods with a status other than Running. Here are the most common issues:

* **Pending**: The pod cannot be scheduled onto a node. This usually means your cluster has run out of resources (CPU or memory). You may need to add more nodes or use larger ones. Use kubectl describe pod \<pod-name\> to see the specific reason.  
* **ImagePullBackOff**: Kubernetes cannot pull the Docker image for the pod. This is almost always caused by:  
  * A typo in the image name or tag in your config.yaml.  
  * The image being in a private repository that the cluster does not have credentials to access.  
* **CrashLoopBackOff**: The container is starting, crashing, and then being restarted by Kubernetes in a loop. This indicates a problem with the application itself. You must check the logs of the crashing pod to find the error.

#### **18.2 Scenario 2: User Can't Log In**

If a user is unable to log in, the JupyterHub logs are the best place to find the reason.

1. **Find the Hub Pod Name**:

```

kubectl get pods -n your-namespace | grep hub

```

4.   **View the Hub Logs**:

```

kubectl logs <hub-pod-name> -n your-namespace -f

```

7. *(The \-f flag will "follow" the logs in real-time.)*

Look for log entries related to the authenticator (e.g., GoogleOAuthenticator). Common causes include:

* The user is not in the allowed\_users list in your config.yaml.  
* The OAuth clientId or clientSecret is incorrect.  
* The callbackUrl is misconfigured in your OAuth provider's settings.

#### **18.3 Scenario 3: The Galyleo Service is Not Working**

If users can log into the Hub but the Galyleo features are unavailable, the issue is likely with the Galyleo Service itself or the connection between it and the Hub.

1. **Check if the Galyleo Service Pod is Running**:

```

kubectl get pods -n your-namespace | grep galyleo-service

```

2.   If it's not in a Running state, debug it like any other pod (see Scenario 1).  
3. **Check the Galyleo Service Logs**:

```

kubectl logs <galyleo-service-pod-name> -n your-namespace -f

```

4. Look for errors related to missing environment variables, incorrect secrets (like the GCP service account key), or a failure to connect to the Datastore or GCS.  
5. Check the Hub Logs for Connection Errors:  
   View the Hub logs as described in Scenario 2\. The custom code in galyleo\_hub.py makes API calls to the service. If the Hub cannot reach the Galyleo Service, you will see connection error messages in its logs. This often points to a networking issue within the Kubernetes cluster.

#### **18.4 Scenario 4: A User's Server Fails to Start**

If a specific user's server fails to launch after they log in, you need to check the logs for their individual pod.

1. **Find the User's Pod Name**: The pod will be named something like jupyter-\<username\>.

```

kubectl get pods -n your-namespace | grep jupyter-

```

2. **Check the User's Pod Logs**:

```

kubectl logs <jupyter-username-pod-name> -n your-namespace -f

```

3. This will show you any errors that occurred when the user's notebook server tried to start, which can help diagnose issues with their specific environment or image.


### **19\. Extensions and New Environments**

One of the most powerful features of a Zero to JupyterHub (Z2JH) deployment is its extensibility. You can easily expand the capabilities of your Hub by adding new user environments (e.g., different Docker containers with specialized tools) and new backend services or extensions.

#### 19.1 **Adding New User Environments**

A "new environment" is a different Docker container that provides users with an alternative set of tools or an entirely different web-based UI, such as a specialized editor. The Z2JH Helm chart makes it simple to offer users a choice of environments when their server starts.

This is managed through the singleuser.profileList section in your config.yaml file.

Each entry in the profileList creates a new option on the user's server spawn page. The key is the kubespawner\_override, which allows you to specify a different Docker image for that option.

##### **19.2 Example: Adding a "Tensorflow" Environment**

To add a new environment that uses a Docker image with Tensorflow pre-installed, you would add an entry like this to your config.yaml:

```

# In your config.yaml
singleuser:
  # ... other singleuser settings
  
  profileList:
    - display_name: "Data Science (Default)"
      description: "Standard data science environment with Galyleo."
      kubespawner_override: 
        image: rickmcgeer/el-jupyter:datascience_0.0.9

    - display_name: "Tensorflow"
      description: "An environment with Tensorflow and GPU support."
      kubespawner_override: 
        image: rickmcgeer/el-jupyter:tensorflow_0.0.9 # <-- The new environment's image
        pullPolicy: Always

```

**Key Requirements:**

* The Docker image for a new environment must provide a web-based interface as its primary UI.  
* The image must be accessible from your Kubernetes cluster (i.e., in a public or configured private container registry).

### **20\. Adding Hub Extensions (Services)**

An "extension" is a backend service that integrates with JupyterHub to provide additional functionality, much like the Galyleo Service itself. These services run as separate Deployments in your Kubernetes cluster and are made available to users through the Hub's proxy.

The Galyleo Service provides the canonical architectural pattern for adding a new extension. The process involves two major steps:

#### **20.1 Step 1: Deploy the Service in Kubernetes**

First, you must deploy your new service as a standard Kubernetes application, typically consisting of a Deployment and a Service. This is done with a dedicated YAML file (like galyleo-service.yaml).

The service must be deployed in the same Kubernetes namespace as your JupyterHub instance so that the Hub's internal networking can discover it.

#### **20.2 Step 2: Integrate the Service with JupyterHub**

Next, you must tell the Hub about your new service and configure its permissions. This is done by injecting custom Python code into the Hub's configuration using the hub.extraConfig section of your config.yaml.

This custom code, typically provided in a separate Python file (like galyleo\_hub.py) and loaded via a ConfigMap, is responsible for:

1. **Registering the service**: Telling the Hub the internal URL of the new service.  
2. **Configuring authentication and permissions**: Defining which users or groups can access the new service.

#### **20.3 Example: The Galyleo Service Integration**

The galyleo\_hub.py script provides a perfect template. It contains a function, setup\_galyleo\_service, which is called from config.yaml. This function programmatically adds the Galyleo service to the Hub's list of services and sets up the necessary access roles.

```

# In galyleo_hub.py (simplified for clarity)

def setup_galyleo_service(c, cluster_url, namespace, api_token):
  # Internal URL for the service
  url = f'http://galyleo-service.{namespace}.svc.cluster.local:5000'
  
  # Register the service with the Hub
  c.JupyterHub.services.append({
      'name': 'galyleo',
      'url': url,
      'api_token': api_token,
      'admin': True
  })

  # Define roles for user access
  c.JupyterHub.load_roles.append({
      'name': 'galyleo-user-role',
      'scopes': ['access:services!service=galyleo'],
      'groups': ['galyleo-users']
  })

```

This modular approach allows you to add any number of powerful backend extensions to your JupyterHub, creating a rich, integrated environment for your users.

## **Part V: Advanced Topics**

### **21\. Advanced Networking: Using a Dedicated VPC**

For production deployments, it is strongly recommended to run your GKE cluster inside a dedicated Virtual Private Cloud (VPC) network rather than the default VPC. This provides significant security and operational benefits.

**Why use a dedicated VPC?**

* **Isolation:** A dedicated VPC creates a private network for your hub, isolating its traffic from other GCP projects and services. This is a critical security measure.  
* **IP Range Control:** It gives you full control over the IP address ranges for your nodes, pods, and services, preventing conflicts with other networks.  
* **Custom Firewall Rules:** You can apply granular firewall rules to your hub's network without affecting other resources in your organization.

**Creating and Using a Dedicated VPC**

First, create the VPC and a subnet within it. Then, reference them when you create the GKE cluster.

```

# Set variables for your configuration
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"
export VPC_NETWORK_NAME="galyleo-hub-vpc"
export SUBNET_NAME="galyleo-hub-subnet"
export CLUSTER_NAME="galyleo-hub-cluster" # Should match your cluster name
export SERVICE_ACCOUNT_EMAIL="galyleo-hub-admin@${PROJECT_ID}.iam.gserviceaccount.com"


# 1. Create the custom VPC network
gcloud compute networks create $VPC_NETWORK_NAME \
  --project=$PROJECT_ID \
  --subnet-mode=custom

# 2. Create a subnet within the VPC
gcloud compute networks subnets create $SUBNET_NAME \
  --project=$PROJECT_ID \
  --network=$VPC_NETWORK_NAME \
  --region=$REGION \
  --range=10.0.4.0/22 # Example IP range, adjust if needed

# 3. Update your cluster creation command to use the new network
# This command replaces the original `gcloud container clusters create`
gcloud container clusters create $CLUSTER_NAME \
  --region $REGION \
  --network $VPC_NETWORK_NAME \
  --subnetwork $SUBNET_NAME \
  --machine-type "e2-standard-2" \
  --num-nodes "1" \
  --node-locations "${REGION}-a,${REGION}-b" \
  --service-account $SERVICE_ACCOUNT_EMAIL \
  --scopes "[https://www.googleapis.com/auth/cloud-platform](https://www.googleapis.com/auth/cloud-platform)"

# Note: Remember to add the --network and --subnetwork flags
# to any `gcloud container node-pools create` commands as well.

```

## **Part VI: Appendix**
### ** 21\. galyleo_hub.py **
```
# galyleo_hub.py
'''
Extensions to JupyterHub for Galyleo.  This involves:
1. Setting up a new authenticator to add users to the
   galyleo-users group to access the Galyleo service
2. Setting up a new spawner to inject the GALYLEO_API_TOKEN
   into the user's environment.
'''
import asyncio
from jupyterhub.orm import User, Group
from oauthenticator.google import GoogleOAuthenticator

class GalyleoAuthenticator(GoogleOAuthenticator):
  '''
  An extension of GoogleOAuthenticator to add users to the
  galyleo-users group to access the Galyleo service.
  Parameters:
    user: a User object
  Returns:
    None
  '''
  async def add_user(self, user):
    self.log.info(f"GalyleoAuthenticator.add_user: user={user.name}")
    result = super().add_user(user)
    if asyncio.iscoroutine(result):
        await result
    else:
        self.log.info(f"User already exists in Hub DB: {user.name}")
    # Get the db user from the database
    hub = self.parent
    orm_user = hub.db.query(User).filter_by(name=user.name).first()
    if orm_user is None:
      self.log.error(f"ORM user not found for {user.name}")
      return
    # Pull the galyleo-users group, creating it if it doesn't exist
    group_name = "galyleo-users"
    group = hub.db.query(Group).filter_by(name=group_name).first()

    if not group:
      self.log.info(f"Creating group: {group_name}")
      group = Group(name=group_name)
      hub.db.add(group)
      hub.db.commit()
    # add the user to the group
    if orm_user not in group.users:
      self.log.info(f"Adding {user.name} to group {group_name}")
      group.users.append(orm_user)
      hub.db.commit()
          
def setup_galyleo_service(c, cluster_url, namespace, galyleo_api_token):
  '''
  Set up the Galyleo Service.  Adds the record for the service to JupyterHub.services, adds the roles for the Galyleo service to talk to the Hub and
  get the user list, and the roles for users to access the Galyleo service.
  Parameters:
    c: the variable containting the JupyterHub
    cluster_url: the url of the cluster, e.g. https://galyleo-beta.engageLively.com
    namespace: the Kubernetes namespace.  Needed for the K8S URL of the service
    galyleo_api_token: the API token for the Galyleo service (token for the service to access the Hub API)
  Returns:
    None
  '''
  url = f'http://galyleo-service.{namespace}.svc.cluster.local:5000'
  oauth_redirect_uri = f'{cluster_url}/services/galyleo/callback'
  c.JupyterHub.services.append(
    {
      'name': 'galyleo',
      'url': url,
      'api_token': galyleo_api_token,
      'oauth_redirect_uri': oauth_redirect_uri,
      'oauth_no_confirm': True,
      'oauth_client_id': 'service-galyleo',
      'oauth_client_allowed_scopes': ['access:services!service=galyleo'],
      'admin': True,
      # 'access': True
    }
  )
  if not hasattr(c.JupyterHub, 'load_roles'):
    c.JupyterHub.load_roles = []
  c.JupyterHub.load_roles.append(
    {
      'name': 'galyleo-role',
      'scopes': ['list:users'],
      'services': ['galyleo'],
    }
  )
  c.JupyterHub.load_roles.append(
    {
      'name': 'galyleo-user-role',
      'scopes': ['access:services!service=galyleo'],
      'roles': ['user', 'users'],
      'groups': ['galyleo-users']
    }
  )
  c.JupyterHub.authenticator_class = GalyleoAuthenticator
  # make sure the URL loads the appropriate environment variables

  c.Spawner.default_url="/lab?inJupyterLab=true&galyleoServer=https://galyleo-beta.engagelively.com&galyleo_storage_server=https://galyleo-beta.engagelively.com/services/galyleo/upload_dashboard"
  
```