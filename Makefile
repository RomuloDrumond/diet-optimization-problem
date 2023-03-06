CONDA_ENV_NAME := dietopt
CONDA_ := $(shell type mamba > /dev/null && echo 'mamba' || echo 'conda')

env-save:
	@$(CONDA_) env export --name $(CONDA_ENV_NAME) --file $(CONDA_ENV_NAME).yml

env-create:
	@$(CONDA_) env create -f $(CONDA_ENV_NAME).yml

env-remove:
	@$(CONDA_) env remove --name $(CONDA_ENV_NAME)