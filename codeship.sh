#!/bin/bash
# Install SDL on Codeship - https://www.libsdl.org
#
SDL_DIR=${SDL_DIR:=$HOME/cache/sdl}

set -e

if [ ! -d "${SDL_DIR}" ]; then
  mkdir -p "${HOME}/sdl"
  wget "https://www.libsdl.org/release/SDL-1.2.15.tar.gz"
  tar -xaf "SDL-1.2.15.tar.gz" --strip-components=1 --directory "${HOME}/sdl"

  (
    cd "${HOME}/sdl" || exit 1
    sed -e '/_XData32/s:register long:register _Xconst long:' \
        -i src/video/x11/SDL_x11sym.h &&
    ./configure --prefix="${SDL_DIR}"
    make
    make install
  )
fi

ln -s "${SDL_DIR}/bin/"* "${HOME}/bin"