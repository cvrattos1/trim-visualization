__run_autobase() {

		echo "-------------------------------------------------------------------"
		echo "Create Basecases"
		script="from CalcSandbox.basecases import basecase;basecase.auto_basecase();"
	echo $script

	printf "$script" | python manage.py shell
	echo "-------------------------------------------------------------------"


}

# Call all functions
__run_autobase
