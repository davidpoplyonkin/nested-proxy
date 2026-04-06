# Nested Proxy
## About
This is a deployment strategy for serving multiple apps from a single VPS, using a single domain. The primary purpose of this is the ease of maintenance. The main challenge is that in a similar setup, all requests (e.g. HTTPS) are delivered to the same port (e.g. 443) of the same IP address, necessitating a proxy, such as Nginx. However, instead of managing a single, bloated Nginx configuration, this architecture distributes the responsibilities across a number of specialized instances:
- **Master Nginx:** Acts as the primary entry point. It listens for all incoming requests and routes them to the correct application based on a subdomain naming convention.
- **App-Specific Nginx Instances:** Each application runs its own Nginx instance connected to the Master Nginx Docker network. These instances handle app-specific logic, such as serving static files or load balancing microservices, without interfering with other apps.

The benefits of this setup include:
- **Scalability:** Adding a new app only requires launching a new container; the Master Nginx handles routing dynamically via the shared network.
- **Separation of Concerns:** Keeps the application logic isolated from the global routing logic.
- **Centralized SSL:** Minimizes overhead by leveraging a single wildcard certificate managed exclusively by the Master Nginx, removing the need for per-app certificate management.
## Getting Started

1. Rent a domain and create a Wildcard A Record (e.g., *.example.com) pointing to the server's IP address.

2. Obtain a wildcard SSL certificate (e.g. via acme.sh) and place the `cert.pem` and `key.pem` files into `master-nginx/certs/`.

3. Search and replace `example.com` in all `nginx.conf` files to reflect the actual domain name.

4. Create a network for the Master Nginx to communicate with app-specific instances:
```
docker network create master-nginx-network
```

5. Ensure that Nginx service names in each app's `docker-compose.yml` follow the convention `<app-name>-nginx`. The Master Nginx relies on these specific hostnames to proxy traffic internally.

6. Start the applications, then the Master Nginx:
```
# Inside each app directory and the master directory
docker compose up -d
```
