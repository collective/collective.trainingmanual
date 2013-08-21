*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/annotate.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser  Setup Plone site
Test Teardown  Close all browsers

** Variables **

${SSDIR}  /tmp/images


*** Test cases ***

Got to control panel
    Given a site owner
     When i go to control panel

*** Keywords ***

Setup Plone site
    Given a site owner
      and a French Plone site
      and mail configured

a site owner
    Enable autologin as  Manager
    Set autologin username  admin

a French Plone site
    Go to  ${PLONE_URL}/@@language-controlpanel
    Select From List  form.default_language  fr
    Click Button  form.actions.save

mail configured
    Go to  ${PLONE_URL}/@@mail-controlpanel
    Input text  name=form.smtp_host  smtp.monfai.fr
    Input text  name=form.smtp_port  25
    Input text  name=form.email_from_name  Webmestre de Plone.fr
    Input text  name=form.email_from_address  webmestre@plone.fr
    Capture and crop page screenshot  ${SSDIR}/parametrage/envoi-courriel.png  css=#content
#    Capture viewport screenshot  ${SSDIR}/parametrage/envoi-courriel.png
#    Capture page screenshot  ${SSDIR}/parametrage/envoi-courriel.png
    Click Button  form.actions.save


i go to control panel
    Go to  ${PLONE_URL}/@@overview-controlpanel
    Capture page screenshot  ${SSDIR}/parametrage/configuration.png
    Capture and crop page screenshot  ${SSDIR}/parametrage/lien-conf-utilisateurs-groupes.png  css=a[href $= "@@usergroup-userprefs"]
