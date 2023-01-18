save-env:
	@conda env export -f dietopt.yml

create-env:
	@conda env create -f dietopt.yml
