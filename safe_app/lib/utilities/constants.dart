import 'package:flutter/material.dart';

const Color kLogoDarkBlueColor = Color(0xFF021B3B);
const Color kLogoTextYellowColor = Color(0xFFFCA311);
const Color kMenuGreyColor = Color(0xFF2E323A);
const Color kMenuLightGreyColor = Color(0xFF282C33);
const Color kDoorIconColor = Color(0xFF72D4B2);
const Color kReportButtonColor = Color(0xFFE5525E);

const TextStyle kBrandTitleYellowTextStyle = TextStyle(
  fontSize: 115.0,
  fontFamily: 'Bebas Neue',
  letterSpacing: 6.0,
  color: kLogoTextYellowColor,
);

const TextStyle kLittleBrandTitleDarkBlueTextStyle = TextStyle(
  fontSize: 30.0,
  fontFamily: 'Bebas Neue',
  letterSpacing: 2.0,
  color: kLogoDarkBlueColor,
);

const TextStyle kMediumBrandTitleDarkBlueTextStyle = TextStyle(
  fontSize: 40.0,
  fontFamily: 'Bebas Neue',
  letterSpacing: 2.0,
  color: kLogoDarkBlueColor,
);

final TextStyle kLittleGreyTextStyle = TextStyle(
  fontSize: 16.0,
  fontFamily: 'Nunito',
  color: Colors.grey[700]
);

const TextStyle kLittleTitleTextStyle = TextStyle(
  fontSize: 20.0,
  fontFamily: 'Nunito',
  fontWeight: FontWeight.bold,
);

const TextStyle kMediumTitleTextStyle = TextStyle(
  fontSize: 30.0,
  fontFamily: 'Nunito',
  fontWeight: FontWeight.bold,
);

const TextStyle kBigTitleTextStyle = TextStyle(
  fontSize: 40.0,
  fontFamily: 'Nunito',
  fontWeight: FontWeight.bold,
);

const TextStyle kButtonBoldWhiteTextStyle = TextStyle(
  fontSize: 16.0,
  fontFamily: 'Nunito',
  fontWeight: FontWeight.bold,
  color: Colors.white
);

const kTableHeaderTextStyle = TextStyle(
    fontSize: 16.0,
    fontFamily: 'Nunito',
    fontWeight: FontWeight.bold,
);

final kInputFieldDecoration = InputDecoration(
  enabledBorder: OutlineInputBorder(
    borderRadius: BorderRadius.circular(5.0),
    borderSide: BorderSide(
        width: 1.0,
        color: Colors.grey
    ),
  ),
  focusedBorder: OutlineInputBorder(
    borderRadius: BorderRadius.circular(5.0),
    borderSide: BorderSide(
        width: 2.0,
        color: Colors.grey
    ),
  ),
  disabledBorder: OutlineInputBorder(
    borderRadius: BorderRadius.circular(5.0),
    borderSide: BorderSide(
        width: 1.0,
        color: Colors.grey.shade300
    ),
  ),
  contentPadding: EdgeInsets.all(12.0),
  isCollapsed: true,
);

final kDarkBlueButtonStyle = ButtonStyle(
  backgroundColor: MaterialStateProperty.all(kLogoDarkBlueColor),
  elevation: MaterialStateProperty.all(5.0),
);