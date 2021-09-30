import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:modal_progress_hud_nsn/modal_progress_hud_nsn.dart';
import 'package:safe_app/components/inputFields/custom_text_form_field.dart';
import 'package:safe_app/services/loading_controller.dart';
import 'package:safe_app/services/safe_api_helper.dart';
import 'package:safe_app/services/safe_app_controller.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class DoorBottomSheetAddForm extends StatelessWidget {

  DoorBottomSheetAddForm({required this.mac, required this.sanitizer});

  final String mac;
  final String sanitizer;

  final _keyForm = GlobalKey<FormState>();
  final SAFEApiHelper _safeApiHelper = SAFEApiHelper();
  final SafeAppController _safeAppController = Get.find();

  final TextEditingController _macController = TextEditingController();
  final TextEditingController _sectorNameController = TextEditingController();
  final TextEditingController _doorNameController = TextEditingController();
  final TextEditingController _sanitizerController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    _macController.text = mac;
    _sanitizerController.text = sanitizer;
    return GetBuilder<LoadingController>(
      init: LoadingController(),
      builder: (loadingController) => ModalProgressHUD(
        inAsyncCall: loadingController.isLoading,
        progressIndicator: CircularProgressIndicator(color: kLogoDarkBlueColor,),
        child: Container(
          decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(20.0),
                topRight: Radius.circular(20.0),
              )
          ),
          padding: EdgeInsets.symmetric(vertical: 10.0, horizontal: 20.0),
          child: SingleChildScrollView(
            child: Form(
              key: _keyForm,
              child: Column(
                children: [
                  Container(
                    width: 70.0,
                    height: 3.0,
                    color: Colors.grey,
                  ),
                  SizedBox(height: 10.0,),
                  Text(
                    'Agregar Puerta',
                    style: kLittleTitleTextStyle,
                  ),
                  SizedBox(height: 10.0,),
                  CustomTextFormField(label: 'MAC', controller: _macController, enabled: false,),
                  CustomTextFormField(label: 'Sector', controller: _sectorNameController,),
                  CustomTextFormField(label: 'Nombre', controller: _doorNameController,),
                  CustomTextFormField(label: 'Sanitizante', controller: _sanitizerController, enabled: false,),
                  SizedBox(height: 5.0,),
                  SizedBox(
                    width: double.infinity,
                    child: TextButton(
                      onPressed: () async {
                        if(_keyForm.currentState!.validate()){
                          loadingController.toggleLoadingState();

                          var res = await _safeApiHelper.addDoor(mac, _sectorNameController.text, _doorNameController.text, sanitizer);

                          if(res == null){
                            await _safeAppController.updateDoorsList();
                            Get.back();
                          } else {
                            Get.snackbar(
                              'Error:',
                              res,
                              colorText: Colors.white,
                              backgroundColor: kLogoDarkBlueColor.withOpacity(0.9),
                              icon: Icon(FontAwesomeIcons.timesCircle, color: Colors.white,),
                              margin: EdgeInsets.symmetric(vertical: 5.0, horizontal: 20.0),
                            );
                          }

                          loadingController.toggleLoadingState();
                        } else {
                          print('not validated');
                        }
                      },
                      child: Text(
                        'Guardar',
                        style: kButtonBoldWhiteTextStyle,
                      ),
                      style: kDarkBlueButtonStyle,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
