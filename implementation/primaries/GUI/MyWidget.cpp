#include <MyWidget.h>

void MyWidget::mousePressEvent(QMouseEvent* event)
{
    event->accept(); // do not propagate
    if (isWindow())
        offset = event->globalPos() - pos();
    else
        offset = event->pos();
}

void MyWidget::mouseMoveEvent(QMouseEvent* event)
{
    event->accept(); // do not propagate
    if (isWindow())
        move(event->globalPos() - offset);
    else
        move(mapToParent(event->pos() - offset));
}

void MyWidget::mouseReleaseEvent(QMouseEvent* event)
{
    event->accept(); // do not propagate
    offset = QPoint();
}