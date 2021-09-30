import 'package:flutter/material.dart';
import 'package:safe_app/utilities/constants.dart';

class IconText extends StatelessWidget {

  IconText({required this.icon, required this.text});

  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    return FittedBox(
      fit: BoxFit.fitWidth,
      child: Row(
        children: [
          Icon(
            icon,
            color: kLogoDarkBlueColor,
          ),
          SizedBox(width: 15.0,),
          Text(
            text,
            style: kLittleGreyTextStyle,
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}