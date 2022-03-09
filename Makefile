.PHONY: all render clean_env clean_tools clean

all: ;

render: all clean_tools
	repo-utils/render.py distros.yaml .

clean_env: ;
	rm -rf _conda/*/

clean_tools: ;
	rm -rf tool_collections/*/ tools/*/

clean: clean_env clean_tools
