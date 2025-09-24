Set-StrictMode -Version Latest
Import-Module "$PSScriptRoot\ForensicsModule.psm1" -Force

function Show-Menu {
    Write-Host "============================="
    Write-Host "   Menú Forense"
    Write-Host "============================="
    Write-Host "1. Exportar eventos a CSV"
    Write-Host "2. Listar procesos y conexiones"
    Write-Host "3. Consultar IPs en AbuseIPDB"
    Write-Host "0. Salir"
}

do {
    Show-Menu
    $choice = Read-Host "Seleccione una opción"

    switch ($choice) {
        "1" {
            $log = Read-Host "Ingrese el log (Application/System/Security)"
            Get-EventsToCsv -LogName $log
        }
        "2" {
            Get-ProcessConnections
        }
        "3" {
            $apiKey = Read-Host "Ingrese su API Key de AbuseIPDB"
            $ips = Read-Host "Ingrese las IPs separadas por coma"
            $ipArray = $ips -split ","
            Get-AbuseIPDBReport -ApiKey $apiKey -IpList $ipArray
        }
        "0" {
            Write-Host "Saliendo..."
        }
        default {
            Write-Host "Opción inválida"
        }
    }
} while ($choice -ne "0")
