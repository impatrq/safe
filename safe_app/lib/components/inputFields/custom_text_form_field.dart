import 'package:flutter/material.dart';
import 'package:safe_app/utilities/constants.dart';

class CustomTextFormField extends StatelessWidget {

  CustomTextFormField({required this.label, this.onChanged, this.enabled = true, this.controller});

  final String label;
  final Function(String)? onChanged;
  final bool enabled;
  final TextEditingController? controller;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: kLittleGreyTextStyle,),
        TextFormField(
          controller: controller,
          onChanged: onChanged,
          decoration: kInputFieldDecoration,
          enabled: enabled,
          validator: (value){
            if (value!.isEmpty) {
              return 'Por favor, ingrese un valor.';
            }
          },
        ),
        SizedBox(height: 10.0,),
      ],
    );
  }
}