import 'package:flutter/material.dart';

class ColoredSafeArea extends StatelessWidget {

  ColoredSafeArea({required this.child});

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      child: SafeArea(
        child: child,
      ),
    );
  }
}