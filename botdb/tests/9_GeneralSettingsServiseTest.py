import unittest
from botdb.services import GeneralSettingsService
from botdb.entities.GeneralSettings import GeneralSettings


class TestQuestionServiceService(unittest.TestCase):
    generalSettingsCheck: GeneralSettings

    def _check_data(self, checking_obj: object, control_obj: object):
        for field in checking_obj.__dict__.keys():
            value = checking_obj.__dict__[field]
            controlValue = control_obj.__dict__[field]
            self.assertEqual(value, controlValue, '{2} should be {0} actual {1}'.format(controlValue, value, field))

    @classmethod
    def setUpClass(cls):
        print('\n[[[   TESTINGGeneralSettingsService  ]]]\n')

    def setUp(self):
        self.generalSettingsCheck = GeneralSettings(updateDelay=60, timeUntilTimeout=30, timeoutsLimit=5,
                                                    bombMessagesTime=15, dialogWindowTime=60)
        GeneralSettingsService.delete_general_settings()
    # =====================

    # =====================
    def test_create_and_get_general_settings(self):
        print('Testing create_general_settings() and get_general_settings()')

        GeneralSettingsService.create_general_settings()
        generalSettings = GeneralSettingsService.get_general_settings()

        self._check_data(control_obj=generalSettings, checking_obj=self.generalSettingsCheck)
        print('Successful\n')
    # =====================

    # =====================
    def test_get_general_settings_count(self):
        print('Testing get_general_settings_count()')

        GeneralSettingsService.create_general_settings()
        answer = GeneralSettingsService.get_general_settings_count()

        self.assertEqual(answer, 1, 'rows_count should be {0} actual {1}'.format(1, answer))
        print('Successful\n')
    # =====================

    # =====================
    def test_get_or_init_general_settings(self):
        print('Testing get_or_init_general_settings()')

        generalSettings = GeneralSettingsService.get_or_init_general_settings()

        self._check_data(control_obj=generalSettings, checking_obj=self.generalSettingsCheck)
        print('Successful\n')
    # =====================

    # =====================
    def test_update_general_settings(self):
        print('Testing update_general_settings()')
        GeneralSettingsService.create_general_settings()

        self.generalSettingsCheck.timeoutsLimit = 10
        self.generalSettingsCheck.updateDelay = 150
        self.generalSettingsCheck.bombMessagesTime = 30
        self.generalSettingsCheck.dialogWindowTime = 120
        self.generalSettingsCheck.timeUntilTimeout = 100

        GeneralSettingsService.update_general_settings(generalSettings=self.generalSettingsCheck)
        generalSettings = GeneralSettingsService.get_general_settings()

        self._check_data(control_obj=generalSettings, checking_obj=self.generalSettingsCheck)
        print('Successful\n')
    # =====================

    # =====================
    def test_delete_general_settings(self):
        print('Testing delete_general_settings()')

        GeneralSettingsService.create_general_settings()
        GeneralSettingsService.delete_general_settings()
        answer = GeneralSettingsService.get_general_settings_count()

        self.assertEqual(answer, 0, 'rows_count should be {0} actual {1}'.format(0, answer))
        print('Successful\n')
    # =====================


if __name__ == '__main__':
    print('boot unit tests')
    unittest.main()
