vps_caddy (écoute sur 80/443) → reçoit gsm.cote7.com
gsm_caddy (écoute seulement sur 7777) → reçoit le trafic de vps_caddy
gsm_app → écoute sur 8000

Le flux est donc :

Internet
    ↓
vps_caddy (:443)
    ↓ reverse_proxy localhost:7777
gsm_caddy (:7777)
    ↓ reverse_proxy gsm_app:8000
gsm_app

---->

  1 - nano /opt/pyproject_template/deploy/proxy/Caddyfile :
 
 (security_headers) {
  header {
    X-Content-Type-Options nosniff
    X-Frame-Options DENY
    Referrer-Policy no-referrer-when-downgrade
    Permissions-Policy "geolocation=()"
  }
}

cryptosgeeks.com {
  import security_headers
  handle {
    reverse_proxy cryptogeeks_frontend:80
  }
}

www.cryptosgeeks.com {
  import security_headers
  handle {
    reverse_proxy cryptogeeks_frontend:80
  }
}

cote7.com {
  import security_headers
  handle /api* {
    reverse_proxy fastapi_backend:8000
  }
  handle /admin* {
    reverse_proxy django_backend:8001
  }
  handle /static* {
    reverse_proxy django_backend:8001
  }
  handle {
    reverse_proxy react_frontend:80
  }
}

www.cote7.com {
  import security_headers
  handle /api* {
    reverse_proxy fastapi_backend:8000
  }
  handle /admin* {
    reverse_proxy django_backend:8001
  }
  handle /static* {
    reverse_proxy django_backend:8001
  }
  handle {
    reverse_proxy react_frontend:80
  }
}

gsm.cote7.com {
    reverse_proxy gsm_app:8000
}



2 - Et dans ls Caddyfile du projet GSM :

:7777 {
    handle {
        reverse_proxy gsm_app:8000
    }
}