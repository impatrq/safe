import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:modal_progress_hud_nsn/modal_progress_hud_nsn.dart';
import 'package:safe_app/components/inputFields/custom_text_form_field.dart';
import 'package:safe_app/components/inputFields/custom_text_field_with_icon_buttons.dart';
import 'package:safe_app/services/nfc_reader.dart';
import 'package:safe_app/services/image_picker.dart';
import 'package:safe_app/services/safe_api_helper.dart';
import 'package:safe_app/services/loading_controller.dart';
import 'package:safe_app/services/safe_app_controller.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:image_picker/image_picker.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class WorkerBottomSheetAddForm extends StatelessWidget {
  final _keyForm = GlobalKey<FormState>();

  final SAFEApiHelper _safeApiHelper = SAFEApiHelper();
  final SafeAppController _safeAppController = Get.find();
  final ImagePickerHelper _imagePickerHelper = ImagePickerHelper();

  final TextEditingController _firstNameController = TextEditingController();
  final TextEditingController _lastNameController = TextEditingController();
  final TextEditingController _phoneNumberController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _addressController = TextEditingController();
  final TextEditingController _cardCodeController = TextEditingController();
  final TextEditingController _imagePathController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return GetBuilder<LoadingController>(
      init: LoadingController(),
      builder: (loadingController) => ModalProgressHUD(
        inAsyncCall: loadingController.isLoading,
        progressIndicator: CircularProgressIndicator(
          color: kLogoDarkBlueColor,
        ),
        child: Container(
          decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(20.0),
                topRight: Radius.circular(20.0),
              )),
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
                  SizedBox(
                    height: 10.0,
                  ),
                  Text(
                    'Agregar Trabajador',
                    style: kLittleTitleTextStyle,
                  ),
                  SizedBox(
                    height: 10.0,
                  ),
                  CustomTextFormField(
                    label: 'Nombre',
                    controller: _firstNameController,
                  ),
                  CustomTextFormField(
                    label: 'Apellido',
                    controller: _lastNameController,
                  ),
                  CustomTextFormField(
                    label: 'Número de Teléfono',
                    controller: _phoneNumberController,
                  ),
                  CustomTextFormField(
                    label: 'E-mail',
                    controller: _emailController,
                  ),
                  CustomTextFormField(
                    label: 'Dirección',
                    controller: _addressController,
                  ),
                  CustomTextFormFieldWithIconButton(
                    controller: _cardCodeController,
                    label: 'ID Tarjeta',
                    icon: FontAwesomeIcons.caretRight,
                    onIconPressed: () {
                      Get.defaultDialog(
                          title: 'Instructivo',
                          content: Text(
                            'Apoye una tarjeta en la parte posterior del dispositivo.',
                            style: kLittleGreyTextStyle,
                            textAlign: TextAlign.center,
                          ),
                          cancel: TextButton(
                            onPressed: () async {
                              await NFCReader.stopSession();
                              Get.back();
                            },
                            child: Text(
                              'Cancelar',
                              style: kLittleGreyTextStyle,
                            ),
                          ));
                      NFCReader.startSession((code) {
                        _cardCodeController.text = code;
                        Get.back();
                      });
                    },
                  ),
                  CustomTextFormFieldWithIconButton(
                    controller: _imagePathController,
                    label: 'Imagen de perfil',
                    icon: FontAwesomeIcons.image,
                    onIconPressed: () async {
                      var path = await Get.bottomSheet(
                        Container(
                          decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.only(
                                topLeft: Radius.circular(20.0),
                                topRight: Radius.circular(20.0),
                              )),
                          child: SingleChildScrollView(
                            child: Column(
                              children: [
                                ListTile(
                                  title:
                                      Text('Seleccionar imagen desde Galería'),
                                  leading: Icon(
                                    FontAwesomeIcons.image,
                                    color: kLogoDarkBlueColor,
                                  ),
                                  onTap: () async {
                                    XFile? photo = await _imagePickerHelper
                                        .getImageFromGallery();
                                    Get.back(result: photo?.path);
                                  },
                                ),
                                ListTile(
                                  title: Text('Tomar una imagen con Cámara'),
                                  leading: Icon(
                                    FontAwesomeIcons.camera,
                                    color: kLogoDarkBlueColor,
                                  ),
                                  onTap: () async {
                                    XFile? photo = await _imagePickerHelper
                                        .getImageFromCamera();
                                    Get.back(result: photo?.path);
                                  },
                                ),
                              ],
                            ),
                          ),
                        ),
                        isScrollControlled: true,
                      );
                      _imagePathController.text = path;
                    },
                  ),
                  SizedBox(
                    height: 5.0,
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: TextButton(
                      onPressed: () async {
                        if (_keyForm.currentState!.validate()) {
                          loadingController.toggleLoadingState();
                          var res = await _safeApiHelper.addWorker(
                              _firstNameController.text,
                              _lastNameController.text,
                              _phoneNumberController.text,
                              _emailController.text,
                              _addressController.text,
                              _cardCodeController.text,
                              _imagePathController.text);
                          if (res == null) {
                            await _safeAppController.updateWorkersList();
                            Get.back();
                          } else {
                            Get.snackbar(
                              'Error:',
                              res,
                              colorText: Colors.white,
                              backgroundColor:
                                  kLogoDarkBlueColor.withOpacity(0.9),
                              icon: Icon(
                                FontAwesomeIcons.timesCircle,
                                color: Colors.white,
                              ),
                              margin: EdgeInsets.symmetric(
                                  vertical: 5.0, horizontal: 20.0),
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
