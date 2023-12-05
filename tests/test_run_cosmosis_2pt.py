import pytest
from cosmosis.runtime.config import Inifile
from cosmosis.runtime.pipeline import LikelihoodPipeline
from blind_2pt_cosmosis.run_cosmosis_2pt import setup_pipeline, modify_settings, run_pipeline, run_cosmosis_togen_2ptdict

def test_modify_settings():
    # Setup
    class MockIni:
        def __init__(self):
            self.__dict__ = {'_sections': {'test': {}, 'output': {}, 'pipeline': {}, 'shear_2pt_eplusb': {}, '2pt_gal': {}, 'fits_nz': {}}}

    ini = MockIni()
    angles_file = 'angles.fits'
    nz_file = 'nz.fits'

    # Exercise
    result = modify_settings(ini, angles_file, nz_file)

    # Verify
    assert result._sections['test']['save_dir'] == ''
    assert result._sections['output']['save_dir'] == ''
    assert result._sections['pipeline']['debug'] == 'F'
    assert result._sections['pipeline']['quiet'] == 'T'
    assert result._sections['shear_2pt_eplusb']['theta_file'] == angles_file
    assert result._sections['2pt_gal']['theta_file'] == angles_file
    assert result._sections['fits_nz']['nz_file'] == nz_file

def test_modify_settings_no_files():
    # Setup
    class MockIni:
        def __init__(self):
            self.__dict__ = {'_sections': {'test': {}, 'output': {}, 'pipeline': {}, 'shear_2pt_eplusb': {}, '2pt_gal': {}, 'fits_nz': {}}}

    ini = MockIni()

    # Exercise
    result = modify_settings(ini)

    # Verify
    assert result._sections['test']['save_dir'] == ''
    assert result._sections['output']['save_dir'] == ''
    assert result._sections['pipeline']['debug'] == 'F'
    assert result._sections['pipeline']['quiet'] == 'T'
    assert 'theta_file' not in result._sections['shear_2pt_eplusb']
    assert 'theta_file' not in result._sections['2pt_gal']
    assert 'nz_file' not in result._sections['fits_nz']

def test_modify_settings_missing_section():
    # Setup
    class MockIni:
        def __init__(self):
            self.__dict__ = {'_sections': {'test': {}, 'output': {}, 'pipeline': {}, 'shear_2pt_eplusb': {}, '2pt_gal': {}}}

    ini = MockIni()
    nz_file = 'nz.fits'

    # Exercise and Verify
    with pytest.raises(ValueError):
        modify_settings(ini, None, nz_file)

def test_setup_pipeline():
    # Setup
    inifile = './src/blind_2pt_cosmosis/cosmosis_files/default_blinding_template.ini'
    angles_file = './src/blind_2pt_cosmosis/cosmosis_files/sim_fiducial.fits'
    nz_file = './src/blind_2pt_cosmosis/cosmosis_files/sim_fiducial.fits'

    # Exercise
    pipeline = setup_pipeline(inifile)
    assert isinstance(pipeline, LikelihoodPipeline)

    # Exercise
    pipeline = setup_pipeline(inifile, angles_file=angles_file)
    assert isinstance(pipeline, LikelihoodPipeline)

    # Exercise
    pipeline = setup_pipeline(inifile, nz_file=angles_file)
    assert isinstance(pipeline, LikelihoodPipeline)

    # Exercise
    pipeline = setup_pipeline(inifile, nz_file=angles_file, angles_file=angles_file)
    assert isinstance(pipeline, LikelihoodPipeline)