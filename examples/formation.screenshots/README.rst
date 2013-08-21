=====================
formation.screenshots
=====================

To regenerate the screenshots::

  bin/robot-server formation.screenshots.testing.ACCEPTANCE
  rm -rf /tmp/images
  mkdir -p /tmp/images/parametrage
  bin/robot -d /tmp/images -v SSDIR:/tmp/images -r NONE -l NONE -o NONE src/formation/screenshots/tests/robot/test_control_panel.robot
  cp /tmp/images/parametrage/* ../../integrateur/source/parametrage/

To regenerate the screenshots and the documentation in one command, you can
do::

  BUILDOUTPATH=/home/vincentfretin/svn/collective.trainingmanual/
  bin/robot -v SSDIR:$BUILDOUTPATH/integrateur/source/ \
  -r NONE -l NONE -o NONE \
  src/formation/screenshots/tests/robot/test_control_panel.robot \
  && (cd $BUILDOUTPATH/integrateur && make html)
