$tablaHash = @{
	"Clave 1"="Valor 1";
	"Clave 2"="Valor 2"
}

$tablaHash['Clave 3']='Valor 3'
$tablaHash['Clave 1']='Nuevo valor'
$tablaHash.Remove('Clave 2')
$tablaHashContainsKey('Clave 1')

$tablaHash.Keys
$tablaHash.Values

foreach($clave in $tablaHash.Keys){ 
	Write-Output "Clave $clave, Valor:$($tablaHash[$clave])"
}