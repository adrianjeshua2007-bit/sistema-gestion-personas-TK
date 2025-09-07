docker run -it --rm ^
    -e DISPLAY=host.docker.internal:0 ^
    -e QT_X11_NO_MITSHM=1 ^
    -v %CD%/person_management.db:/app/person_management.db ^
    -v %CD%:/app ^  # ¡ESTA LÍNEA NUEVA ES IMPORTANTE!
    -v /tmp/.X11-unix:/tmp/.X11-unix ^
    --network host ^
    sistema-gestion-personas