import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/services/icon_state_controller.dart';

class CustomLoginField extends StatelessWidget {

  CustomLoginField({this.textEditingController, required this.labelText, this.prefixIcon, this.isPasswordField = false});

  final TextEditingController? textEditingController;
  final String labelText;
  final Icon? prefixIcon;
  final bool isPasswordField;

  Icon _getSuffixIcon(bool showPassword){
    if(showPassword == true){
      return Icon(
        FontAwesomeIcons.solidEyeSlash,
        size: 18.0,
        color: Colors.grey[400],
      );
    } else {
      return Icon(
        FontAwesomeIcons.solidEye,
        size: 18.0,
        color: Colors.grey[400],
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          labelText,
          style: kLittleGreyTextStyle.copyWith(color: Colors.black, fontWeight: FontWeight.bold),
        ),
        GetBuilder<IconController>(
          init: IconController(),
          builder: (controller) => TextField(
            controller: textEditingController,
            style: TextStyle(
                color: Colors.black,
                fontSize: 18.0
            ),
            obscureText: isPasswordField ? !controller.showLoginPassword : false,
            decoration: InputDecoration(
              prefixIcon: prefixIcon,
              suffixIcon: isPasswordField ? GestureDetector(
                child: _getSuffixIcon(controller.showLoginPassword),
                onTap: (){
                  controller.toggleShowLoginPassword();
                },
              ) : null,
              enabledBorder: UnderlineInputBorder(
                  borderSide: BorderSide(
                      color: Colors.grey.shade400,
                      width: 1.0
                  )
              ),
              focusedBorder: UnderlineInputBorder(
                  borderSide: BorderSide(
                      color: Colors.grey.shade700,
                      width: 2.0
                  )
              ),
            ),
          ),
        ),
      ],
    );
  }
}