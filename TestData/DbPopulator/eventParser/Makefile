BINS_RL := $(wildcard *.xml) parserOrder.csv 
INSTALL_BIN_DEST = /opt/phoenix/config/xml

include $(PHOENIX_PATH)/src/cpp/Makefile.inc

build:
	cp -f $(BINS_RL) $(BUILD_CFG_DEST)/xml
