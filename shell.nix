{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python311
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc
    ]}
    echo "Activated work-hm-project dev environment."
    export PYTHONNOUSERSITE="true"
  '';
}

    #   nativeBuildInputs = with pkgs; [
    #playwright-driver.browsers
  #];
    # mkdir -p .env/playwright-browsers
    # ln -sf ${pkgs.playwright-driver.browsers} .env/playwright-browsers
    # export PLAYWRIGHT_BROWSERS_PATH="$(pwd)/.env/playwright-browsers"

    # export PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS=true

  #   export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
  #     pkgs.stdenv.cc.cc
  #     pkgs.glib
  #     pkgs.gtk3
  #     pkgs.nss
  #     pkgs.nspr
  #     pkgs.dbus
  #     pkgs.at-spi2-core
  #     pkgs.xdg-utils
  #     pkgs.libxkbcommon
  #     pkgs.cairo
  #     pkgs.pango
  #     pkgs.freetype
  #     pkgs.fontconfig
  #     pkgs.cups
  #     pkgs.expat
  #     pkgs.xorg.libxcb
  #     pkgs.xorg.libX11
  #     pgkgs.pkgs.xorg.libXcomposite
  #   ]}:$LD_LIBRARY_PATH