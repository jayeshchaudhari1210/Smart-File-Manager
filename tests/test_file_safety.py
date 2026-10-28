import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from fileops import duplicate_candidates, same_content
import main


class FileSafetyTests(unittest.TestCase):
    def test_copy_like_names_with_different_content_are_not_duplicates(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder)
            (p/'a.txt').write_text('original')
            (p/'a (1).txt').write_text('different')
            self.assertEqual(duplicate_candidates(p), [])

    def test_identical_files_keep_original_and_ignore_directories(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder)
            (p/'a.txt').write_bytes(b'same')
            (p/'a (1).txt').write_bytes(b'same')
            (p/'folder').mkdir()
            self.assertEqual(duplicate_candidates(p), [(p/'a (1).txt',p/'a.txt')])
            (p/'a (1).txt').write_bytes(b'changed')
            self.assertFalse(same_content(p/'a (1).txt',p/'a.txt'))

    def test_deletion_uses_trash_without_direct_removal(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder)/'valuable.txt'; p.write_text('keep')
            with patch.object(main,'send2trash') as trash:
                self.assertTrue(main.del_file(str(p)))
                trash.assert_called_once_with(str(p))
                self.assertTrue(p.exists())

    def test_trash_failure_does_not_fall_back_to_permanent_deletion(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'valuable.txt';p.write_text('keep')
            with patch.object(main,'send2trash',side_effect=OSError('unavailable')), patch.object(main.Messagebox,'show_error'):
                self.assertFalse(main.del_file(str(p)))
            self.assertTrue(p.exists())

    def test_delete_shortcut_calls_popup_without_arguments(self):
        with patch.object(main,'del_file_popup') as popup:
            main.wrap_del(None)
            popup.assert_called_once_with()

    def test_zero_match_search_stays_empty(self):
        with tempfile.TemporaryDirectory() as folder:
            previous=os.getcwd();os.chdir(folder)
            try:
                Path('visible.txt').write_text('x')
                tree=Mock();tree.get_children.return_value=[]
                with patch.object(main,'items',tree),patch.object(main,'cwdLabel',Mock()),patch.object(main,'footer',Mock()):
                    main.refresh([])
                self.assertEqual(main.fileNames,[])
                tree.insert.assert_not_called()
            finally:os.chdir(previous)

    def test_copy_progress_polls_without_blocking_gui(self):
        top=Mock();thread=Mock();thread.is_alive.return_value=False
        gauge=Mock()
        with patch.object(main.ttk,'Toplevel',return_value=top),patch.object(main.ttk,'Floodgauge',return_value=gauge),patch.object(main,'refresh') as refresh:
            main.paste_popup(thread,[])
            thread.join.assert_not_called()
            callback=top.after.call_args.args[1];callback()
            refresh.assert_called_once_with()
            top.destroy.assert_called_once_with()


if __name__=='__main__':unittest.main()
