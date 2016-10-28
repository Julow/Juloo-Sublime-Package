THEMES = theme_5

all: $(addsuffix .tmTheme,$(addprefix ../,$(THEMES)))

../%.tmTheme: %
	./gen_theme.py < $< > $@
