import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/components/inputFields/custom_login_field.dart';
import 'package:safe_app/components/customWidgets/url_launcher_icon.dart';
import 'package:safe_app/screens/dashboard_screen.dart';
import 'package:safe_app/services/auth_controller.dart';
import 'package:safe_app/services/icon_state_controller.dart';
import 'package:safe_app/services/safe_app_controller.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/services/safe_api_helper.dart';
import 'package:safe_app/services/loading_controller.dart';
import 'package:modal_progress_hud_nsn/modal_progress_hud_nsn.dart';

class LoginScreen extends StatelessWidget {

  final _safeApiHelper = SAFEApiHelper();
  final AuthController _authController = AuthController();
  final SafeAppController _safeAppController = Get.find();

  final TextEditingController _identifierController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool? keepLoggedIn = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      body: GetBuilder<LoadingController>(
        init: LoadingController(),
        builder: (loadingController) => ModalProgressHUD(
          inAsyncCall: loadingController.isLoading,
          progressIndicator: CircularProgressIndicator(color: kLogoDarkBlueColor,),
          child: Padding(
              padding: EdgeInsets.all(50.0),
              child: Column(
                children: [
                  Expanded(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Hero(
                          tag: 'logo',
                          child: Image.asset('assets/images/safe_logo.png', width: 100.0, height: 100.0,),
                        ),
                        SizedBox(height: 50.0,),
                        Text(
                          'Iniciar Sesión',
                          style: kMediumTitleTextStyle,
                        ),
                        SizedBox(height: 10.0,),
                        Text(
                          '¡Hola! Qué gusto verte de nuevo.',
                          style: kLittleGreyTextStyle,
                        ),
                        SizedBox(height: 25.0,),
                        CustomLoginField(
                          textEditingController: _identifierController,
                          labelText: 'E-mail / Usuario / Telefono',
                          prefixIcon: Icon(
                            FontAwesomeIcons.userAlt,
                            color: Colors.grey.shade400,
                            size: 18.0,
                          ),
                        ),
                        SizedBox(height: 20.0,),
                        CustomLoginField(
                          textEditingController: _passwordController,
                          labelText: 'Contraseña',
                          prefixIcon: Icon(
                            FontAwesomeIcons.key,
                            color: Colors.grey.shade400,
                            size: 18.0,
                          ),
                          isPasswordField: true,
                        ),
                        Row(
                          children: [
                            GetBuilder<IconController>(
                              init: IconController(),
                              builder: (controller) => Checkbox(
                                value: controller.keepLoggedIn,
                                onChanged: (value){
                                  controller.setKeepLoggedIn(value);
                                  keepLoggedIn = value;
                                },
                                fillColor: MaterialStateProperty.all(kLogoDarkBlueColor),
                              ),
                            ),
                            Text('Mantener la sesión iniciada.', style: kLittleGreyTextStyle,)
                          ],
                        ),
                        SizedBox(height: 25.0,),
                        SizedBox(
                          height: 45.0,
                          child: TextButton(
                            onPressed: () async {
                              loadingController.toggleLoadingState();

                              var loginResult = await _safeApiHelper.login(_identifierController.text, _passwordController.text, keepLoggedIn);

                              if(loginResult == null){
                                await _safeAppController.initialize();

                                var userData = await _authController.getLoggedInUserData();

                                Get.offAll(() => DashboardScreen(
                                  userData: userData,
                                ));

                              } else {
                                Get.snackbar(
                                  'Error:',
                                  loginResult,
                                  colorText: Colors.white,
                                  backgroundColor: kLogoDarkBlueColor.withOpacity(0.9),
                                  icon: Icon(FontAwesomeIcons.timesCircle, color: Colors.white,),
                                  margin: EdgeInsets.symmetric(vertical: 5.0, horizontal: 20.0),
                                );
                              }

                              loadingController.toggleLoadingState();
                            },
                            child: Text(
                              'Iniciar Sesión',
                              style: kButtonBoldWhiteTextStyle,
                            ),
                            style: kDarkBlueButtonStyle,
                          ),
                        ),
                        SizedBox(height: 50.0,),
                      ],
                    ),
                  ),
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          '¿Necesitas ayuda? Contáctanos',
                          style: kLittleGreyTextStyle,
                        ),
                      ),
                      UrlLauncherIcon(icon: FontAwesomeIcons.instagram, url: 'https://instagram.com/safe_project'),
                      SizedBox(width: 10.0,),
                      UrlLauncherIcon(icon: FontAwesomeIcons.github, url: 'https://github.com/impatrq/SAFE')
                    ],
                  ),
                ],
              )
          ),
        ),
      ),
    );
  }
}