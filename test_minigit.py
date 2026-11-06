import unittest

from minigit import MiniGit


class MiniGitTests(unittest.TestCase):
    def test_commit_e_pais(self):
        repo = MiniGit()
        primeiro = repo.commitar("início")
        segundo = repo.commitar("segunda alteração")
        self.assertEqual(primeiro, "c1")
        self.assertEqual(repo.pais(primeiro), ())
        self.assertEqual(repo.pais(segundo), (primeiro,))
        self.assertEqual(repo.mensagem(segundo), "segunda alteração")

    def test_busca_e_medicao(self):
        repo = MiniGit()
        repo.commitar("primeiro")
        segundo = repo.commitar("corrige erro")
        self.assertEqual(repo.buscar("erro"), segundo)
        self.assertEqual(repo.medir(), 2)
        self.assertEqual(repo.passos, 2)
        self.assertIsNone(repo.buscar("inexistente"))
        self.assertEqual(repo.medir(), 2)

    def test_branches_e_merge(self):
        repo = MiniGit()
        base = repo.commitar("base")
        repo.criar_branch("feature")
        repo.commitar("main change")
        repo.trocar_branch("feature")
        feature_commit = repo.commitar("feature change")
        repo.trocar_branch("main")
        merge = repo.mesclar("feature")
        self.assertEqual(repo.pais(merge), ("c2", feature_commit))
        self.assertEqual(repo.log(), (merge, "c2", feature_commit, base))
        self.assertEqual(repo.merges(), (merge,))

    def test_log_sem_commits_e_erros(self):
        repo = MiniGit()
        self.assertEqual(repo.log(), ())
        self.assertEqual(repo.medir(), 0)
        with self.assertRaises(ValueError):
            repo.commitar("  ")
        with self.assertRaises(ValueError):
            repo.pais("desconhecido")
        with self.assertRaises(ValueError):
            repo.criar_branch("feature")

    def test_merge_invalido(self):
        repo = MiniGit()
        repo.commitar("base")
        with self.assertRaises(ValueError):
            repo.mesclar("main")
        with self.assertRaises(ValueError):
            repo.mesclar("ausente")


if __name__ == "__main__":
    unittest.main()
