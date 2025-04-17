import argostranslate.package
import argostranslate.translate

class Translator:
    def __init__(self):
        """Initialize the translator"""
        self.from_code = "en"
        self.to_code = "ja"

        # Download and install Argos Translate package
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            filter(
                lambda x: x.from_code == self.from_code and x.to_code == self.to_code, available_packages
            )
        )
        argostranslate.package.install_from_path(package_to_install.download())


    def translate_text(self, text):
        return argostranslate.translate.translate(text, self.from_code, self.to_code)
