.PHONY: clone-openwrt configure update-feeds uninstall-feeds defconfig build upload-build clean-openwrt reset build-debug

clone-openwrt:
	./tools/clone-openwrt.sh

configure:
	python tools/configure.py

update-feeds:
	cd openwrt && ./scripts/feeds update -a
	cd openwrt && ./scripts/feeds install -a

uninstall-feeds:
	cd openwrt && ./scripts/feeds uninstall -a

defconfig:
	cd openwrt && make defconfig

build:
	cd openwrt && make -j$(nproc) download clean world

build-debug:
	cd openwrt && make -j1 V=s

upload-build:
	python tools/upload-build.py

clean-openwrt:
	cd openwrt && make clean

reset:
	rm -rf openwrt
