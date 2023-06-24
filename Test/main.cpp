//
// Created by tony_ on 6/24/2023.
//


#include <QApplication>
#include <QCamera>
#include <QCameraViewfinder>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QCamera *camera = new QCamera;
    QCameraViewfinder *viewfinder = new QCameraViewfinder;

    camera->setViewfinder(viewfinder);

    camera->start();
    viewfinder->show();

    int returnVal = app.exec();

    delete viewfinder;
    delete camera;

    return returnVal;
}
