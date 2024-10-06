# Talks

This directory contains slides and recordings of talks related to `fret-to-robot`.

## Level Up Your Embedded Testing Game – FRETish, Robot, and Twister: A Dream Team

* **Date**: September 17, 2024
* **Event**: Open Source Summit Europe, Vienna
* **Slides**: [20240917 OSS Europe Level Up Your Embedded Testing Game.pdf](20240917%20OSS%20Europe%20Level%20Up%20Your%20Embedded%20Testing%20Game.pdf)
* **Recording**: [Level Up Your Embedded Testing Game – Christian Schlotter, ZEISS & Tobias Kästner, inovex](https://www.youtube.com/watch?v=ndQzEjUiXc4)
  (part of [Zephyr @ OSS EU 2024 playlist on YouTube](https://www.youtube.com/watch?v=X3t240T_-nM&list=PLbzoR-pLrL6qIlWuafNzT5k19Yi16OF27&pp=iAQB))
* **Abstract**:

  Developing embedded software for regulated environments like medical devices presents unique challenges. Crucially,
  we need to document how the software design fulfills stated product requirements. While functional testing remains
  dominant for verifying functional suitability, deriving and maintaining effective test suites can quickly become
  cumbersome.

  This talk explores a novel approach to this longstanding problem. We leverage NASA's FRETish method for formally
  capturing requirements. We will talk about how the formal nature of FRETish requirements allows for automatic test
  case generation leveraging the Robot Framework. The latter was specifically chosen as it is partially supported by
  Zephyr's test harness today and allows to utilize twister for automated test execution of these test suites on real
  hardware. This method has the potential to streamline testing, offering benefits such as reduced time and
  maintenance efforts as well as accurate coverage metrics from very early on in the project's lifecycle.

  We'll discuss our progress in implementing this approach, the challenges we encountered, and potential solutions for
  deeper integration with the Zephyr project.
