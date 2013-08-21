=====================
formation.screenshots
=====================

To regenerate the screenshots::

  bin/robot-server formation.screenshots.testing.ACCEPTANCE
  rm -rf images
  mkdir -p images/parametrage
  bin/robot -d images -r NONE -l NONE -o NONE src/formation/screenshots/tests/robot/test_control_panel.robot
  cp images/parametrage/* ../../integrateur/source/parametrage/
