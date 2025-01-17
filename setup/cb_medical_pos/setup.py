import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        "depends_override": {
            "account_journal_inter_company": "git+https://github.com/tegin/cb-addons.git@14.0#subdirectory=setup/account_journal_inter_company",
            "pos_inter_company": "git+https://github.com/tegin/cb-addons.git@14.0#subdirectory=setup/pos_inter_company",
        }
    },
)
