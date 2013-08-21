=====================
formation.screenshots
=====================

To regenerate the screenshots::

  bin/robot-server formation.screenshots.testing.ACCEPTANCE
  rm -rf /tmp/images
  mkdir -p /tmp/images/parametrage
  bin/robot -d /tmp/images -v SSDIR:/tmp/images -r NONE -l NONE -o NONE src/formation/screenshots/tests/robot/test_control_panel.robot
  cp /tmp/images/parametrage/* ../../integrateur/source/parametrage/
