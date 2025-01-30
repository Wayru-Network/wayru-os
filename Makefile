OPENWRT_DIR := openwrt
TOOLS_DIR := tools

.PHONY: clone-openwrt configure update-feeds uninstall-feeds add-patches defconfig build upload-build clean-openwrt reset build-debug

clone-openwrt:
	$(TOOLS_DIR)/clone-openwrt.sh

update-feeds:
	cd $(OPENWRT_DIR) && ./scripts/feeds update -a
	cd $(OPENWRT_DIR) && ./scripts/feeds install -a

uninstall-feeds:
	cd $(OPENWRT_DIR) && ./scripts/feeds uninstall -a

add-patches:
	python $(TOOLS_DIR)/add_patches.py

configure:
	python $(TOOLS_DIR)/configure.py

defconfig:
	exec $(MAKE) -C $(OPENWRT_DIR) defconfig

build:
	exec $(MAKE) -C $(OPENWRT_DIR) -j$(nproc) download
	exec $(MAKE) -C $(OPENWRT_DIR) -j$(nproc) clean
	exec $(MAKE) -C $(OPENWRT_DIR) -j$(nproc) world

build-debug:
	exec $(MAKE) -C $(OPENWRT_DIR) -j1 V=s

upload-build:
	python $(TOOLS_DIR)/upload-build.py

clean-openwrt:
	cd $(OPENWRT_DIR) && $(MAKE) clean

reset:
	rm -rf $(OPENWRT_DIR) || echo "OpenWRT directory not found, skipping..."
