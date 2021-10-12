import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/components/customWidgets/icon_text.dart';

class WorkerDescriptionSheet extends StatelessWidget {
  WorkerDescriptionSheet(
      {required this.imageURL,
      required this.name,
      required this.address,
      required this.phoneNumber,
      required this.email});

  final String imageURL;
  final String name;
  final String address;
  final String phoneNumber;
  final String email;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(vertical: 10.0, horizontal: 20.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(20.0),
          topRight: Radius.circular(20.0),
        ),
      ),
      child: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              width: 70.0,
              height: 3.0,
              color: Colors.grey,
            ),
            Align(
              alignment: Alignment.centerRight,
              child: Text(
                'Trabajador',
                style: kLittleGreyTextStyle,
              ),
            ),
            Divider(
              thickness: 3,
              color: Colors.grey[300],
            ),
            Row(
              children: [
                Expanded(
                  child: CircleAvatar(
                    radius: 90.0,
                    backgroundColor: Colors.transparent,
                    backgroundImage: NetworkImage(imageURL),
                  ),
                ),
                SizedBox(
                  width: 20.0,
                ),
                Expanded(
                  child: Column(
                    children: [
                      Text(
                        name,
                        style: kLittleTitleTextStyle,
                        textAlign: TextAlign.center,
                      ),
                      SizedBox(
                        height: 15.0,
                      ),
                      IconText(
                          icon: FontAwesomeIcons.mapMarkerAlt, text: address),
                      SizedBox(
                        height: 15.0,
                      ),
                      IconText(
                          icon: FontAwesomeIcons.phoneAlt, text: phoneNumber),
                      SizedBox(
                        height: 15.0,
                      ),
                      IconText(
                          icon: FontAwesomeIcons.solidEnvelope, text: email),
                    ],
                  ),
                ),
              ],
            ),
            Divider(
              thickness: 3,
              color: Colors.grey[300],
            ),
          ],
        ),
      ),
    );
  }
}
