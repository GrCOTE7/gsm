# ============================================================================
#  n8n-bridge.ps1 - Pont local n8n (Docker) -> navigateur Windows
#
#  n8n tourne dans Docker et ne peut pas ouvrir de navigateur sur l'hôte.
#  Ce petit serveur HTTP écoute sur le port 8123 du PC Windows.
#  Quand n8n appelle  /open?url=<url-encodee>  , il ouvre l'URL dans le
#  navigateur par defaut de Windows.
#
#  Lancer (a chaque demarrage) :
#     powershell -ExecutionPolicy Bypass -File scripts\n8n-bridge.ps1
#
#  Depuis n8n, appeler :
#     http://host.docker.internal:8123/open?url=https%3A%2F%2Flaravel.sillo.org%2F
# ============================================================================

param(
    [int]$Port = 8123
)

function Send-HttpResponse {
    param($Client, $Status, $Body)
    $bytes  = [Text.Encoding]::UTF8.GetBytes($Body)
    $header = "HTTP/1.1 $Status`r`n" +
              "Content-Type: text/plain; charset=utf-8`r`n" +
              "Content-Length: $($bytes.Length)`r`n" +
              "Connection: close`r`n`r`n"
    $out = [Text.Encoding]::UTF8.GetBytes($header)
    $Client.GetStream().Write($out, 0, $out.Length)
    $Client.GetStream().Write($bytes, 0, $bytes.Length)
}

try {
    $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $Port)
    $listener.Start()
}
catch {
    Write-Host "ERREUR : impossible d'ecouter sur le port $Port. Verifie qu'il est libre." -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Pont n8n -> navigateur actif" -ForegroundColor Cyan
Write-Host " Ecoute sur : http://0.0.0.0:$Port" -ForegroundColor Cyan
Write-Host " Depuis n8n : http://host.docker.internal:$Port/open?url=<url>" -ForegroundColor Cyan
Write-Host " Ctrl+C pour arreter." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

while ($true) {
    $client = $null
    try {
        $client = $listener.AcceptTcpClient()
        $stream = $client.GetStream()
        $reader = [IO.StreamReader]::new($stream, [Text.Encoding]::UTF8)

        $requestLine = $reader.ReadLine()
        if (-not $requestLine) { continue }

        Write-Host "Requete recue : $requestLine" -ForegroundColor DarkGray
        $parts = $requestLine.Split(' ')
        if ($parts.Count -lt 2) { continue }
        $path = $parts[1]

        if ($path -match '^/open\?url=(.+)$') {
            $url = [Uri]::UnescapeDataString($Matches[1])
            if ($url -match '^https?://') {
                Start-Process $url
                Write-Host "  -> Ouverture dans le navigateur : $url" -ForegroundColor Green
                Send-HttpResponse -Client $client -Status "200 OK" -Body "OK: $url"
            }
            else {
                Write-Host "  -> URL invalide (http/https attendu) : $url" -ForegroundColor Yellow
                Send-HttpResponse -Client $client -Status "400 Bad Request" -Body "URL invalide"
            }
        }
        else {
            Send-HttpResponse -Client $client -Status "404 Not Found" -Body "Utilisation : /open?url=<url-encodee>"
        }
    }
    catch {
        Write-Host "Erreur : $($_.Exception.Message)" -ForegroundColor Red
    }
    finally {
        if ($client) { try { $client.Close() } catch {} }
    }
}
