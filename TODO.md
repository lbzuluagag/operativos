
# pendiente 

- mensajes {cmd:info, src:GUI, dst:APP, msg: "APP1"}
- mensajes {cmd:info, src:GUI, dst:APP, msg: "HALT"}
- mensajes {cmd:info, src:GUI, dst:FILE, msg: "create "}

# comandos para la creacion de carpetas

- mensajes {cmd:info, src:GUI, dst:FILE, msg: "CRE:nombre_carpeta"}
- mensajes {cmd:info, src:GUI, dst:FILE, msg: "DEL:nombre_carpeta"}
- LOG:mensaje (PENDIENTE DETERMINAR QUE VOY A GUARDAR EN EL LOG, TODO ESE MENSAJE O LO QUE VENGA EN EL LOG)
- mensajes {cmd:info, src:GUI, dst:FILE, msg: "LOG:nombre_carpeta"}

# comandos listos
- CRE:nombre_carpeta
- DEL:nombre_carpeta