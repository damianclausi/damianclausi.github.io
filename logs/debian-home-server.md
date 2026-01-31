# Setting Up a Debian Home Server with Docker

> Building a personal homelab for media services and network automation.

---

## The Goal

Create a low-power, always-on server that handles:
- Media streaming (Plex/Jellyfin)
- File synchronization
- Network monitoring
- Container orchestration

## Hardware

I repurposed an old laptop with:
- Intel i5 (4th gen)
- 8GB RAM
- 500GB SSD + 2TB external HDD

## Step 1: Install Debian

Downloaded Debian 12 (Bookworm) netinst ISO and installed with minimal packages:

```bash
# During installation, only select:
# - SSH server
# - Standard system utilities
```

## Step 2: Initial Configuration

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y curl wget git htop neofetch ufw

# Configure firewall
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Step 3: Install Docker

```bash
# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add the repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
```

## Step 4: Docker Compose Stack

Created a `docker-compose.yml` for all services:

```yaml
version: '3.8'

services:
  portainer:
    image: portainer/portainer-ce
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    restart: unless-stopped

  jellyfin:
    image: jellyfin/jellyfin
    ports:
      - "8096:8096"
    volumes:
      - ./jellyfin/config:/config
      - ./media:/media
    restart: unless-stopped

  pihole:
    image: pihole/pihole
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "8080:80/tcp"
    environment:
      TZ: 'America/Argentina/Buenos_Aires'
    volumes:
      - ./pihole/etc:/etc/pihole
      - ./pihole/dnsmasq:/etc/dnsmasq.d
    restart: unless-stopped

volumes:
  portainer_data:
```

## Results

- 24/7 uptime with ~15W power consumption
- All services accessible via local network
- Easy backup with Docker volumes
- Learning Linux administration hands-on

---

*Posted: 2025-12-25*
