.PHONY: clone-openwrt configure feeds defconfig build upload-build clean-openwrt

clone-openwrt:
	./tools/clone-openwrt.sh

configure:
	python tools/configure.py

feeds:
	cd openwrt && ./scripts/feeds update -a
	cd openwrt && ./scripts/feeds install -a

defconfig:
	cd openwrt && make defconfig

build:
	cd openwrt && make -j$(nproc) download clean world

upload-build:
	python tools/upload-build.py

clean-openwrt:
	rm -rf openwrt
