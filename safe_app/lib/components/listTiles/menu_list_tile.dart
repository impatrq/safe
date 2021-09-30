import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:safe_app/services/safe_app_controller.dart';

class MenuListTile extends StatelessWidget {

  MenuListTile({required this.label, required this.icon, required this.onTap,});

  final String label;
  final IconData icon;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(
        icon,
        size: 24.0,
      ),
      title: Text(
          label,
          style: TextStyle(
            fontSize: 18.0,
            fontFamily: 'Nunito',
          )
      ),
      onTap: onTap,
    );
  }
}