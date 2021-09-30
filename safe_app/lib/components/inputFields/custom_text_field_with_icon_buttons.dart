import 'package:flutter/material.dart';
import 'package:safe_app/utilities/constants.dart';

class CustomTextFormFieldWithIconButton extends StatelessWidget {

  CustomTextFormFieldWithIconButton({required this.label, required this.icon, required this.onIconPressed, this.onChanged, this.controller});

  final String label;
  final IconData icon;
  final VoidCallback onIconPressed;
  final Function(String)? onChanged;
  final TextEditingController? controller;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: kLittleGreyTextStyle,),
        Row(
          children: [
            Flexible(
              child: TextFormField(
                controller: controller,
                onChanged: onChanged,
                decoration: kInputFieldDecoration,
                enabled: false,
                validator: (value){
                  if(value!.isEmpty){
                    return 'Por favor, ingrese un valor.';
                  }
                },
              ),
            ),
            IconButton(
              onPressed: onIconPressed,
              icon: Icon(
                icon,
                color: kLogoDarkBlueColor,
              ),
            )
          ],
        ),
        SizedBox(height: 10.0,),
      ],
    );
  }
}
