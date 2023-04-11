"""Module that contains code for displaying dialog for selecting videos."""

from typing import List
from qtpy.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox

# from sleap.gui.commands import CommandContext
from sleap.gui.dataviews import GenericTableView, VideosTableModel
from sleap.io.video import Video


class SelectVideosDialog(QDialog):
    """Opens `QDialog` to select videos from a list of videos in the project."""

    def __init__(self, context: "CommandContext", videos: List[Video]):
        super().__init__()
        self.selected_videos = []
        self.model = VideosTableModel(items=videos, context=context)
        self.table = GenericTableView(
            state=context.app.state,
            row_name="video",
            is_activatable=True,
            model=self.model,
            is_multiselect=True,
            ellipsis_left=True,
        )

        # Pop up a widget to select the videos
        self.setWindowTitle("Add videos to session")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.table)

        # Connect the OK button to the accept method
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok, self)
        self.buttonBox.accepted.connect(self.accept)
        self.layout().addWidget(self.buttonBox)

    # Allow the user to select multiple videos
    def accept(self):
        self.selected_videos = self.table.getSelectedRowItems()
        super().accept()

    def result(self) -> List[Video]:
        return self.selected_videos


if __name__ == "__main__":
    import os

    from qtpy import QtWidgets

    import sleap
    from sleap.gui.commands import CommandContext

    app = QtWidgets.QApplication()

    ds = os.environ["ds-many-videos"]
    labels = sleap.load_file(ds)
    context = CommandContext.from_labels(labels=labels)
    dialog = SelectVideosDialog(context, labels.videos)
    dialog.show()
    dialog.exec_()
    result = dialog.result()
    print(result)
